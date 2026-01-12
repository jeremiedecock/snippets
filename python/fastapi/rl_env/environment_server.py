from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import anyio
import gymnasium as gym
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel


# ----------------- Configuration -----------------
ALLOWED_TOKENS = {
    # tokens pré-définis (exemples)
    "team_001_token",
    "team_002_token",
    "team_003_token",
}

ENV_ID = "FrozenLake-v1"
MAX_STEPS_PER_EPISODE = 10_000
SESSION_TTL_SECONDS = 30 * 60  # 30 min d'inactivité


# ----------------- Modèles API -----------------
class ResetRequest(BaseModel):
    seed: Optional[int] = None
    options: Optional[Dict[str, Any]] = None


class ResetResponse(BaseModel):
    observation: Any
    info: Dict[str, Any]


class StepRequest(BaseModel):
    action: int


class StepResponse(BaseModel):
    observation: Any
    reward: float
    terminated: bool
    truncated: bool
    info: Dict[str, Any]
    step_count: int


# ----------------- Stockage par token -----------------
@dataclass
class UserEnvState:
    env: gym.Env
    lock: anyio.Lock = field(default_factory=anyio.Lock)
    last_seen: float = field(default_factory=time.time)
    step_count: int = 0


USER_ENVS: Dict[str, UserEnvState] = {}


# ----------------- Auth -----------------
def get_token(authorization: Optional[str] = Header(default=None)) -> str:
    """
    Attend: Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization format (use Bearer token)")
    token = parts[1]
    if token not in ALLOWED_TOKENS:
        raise HTTPException(status_code=403, detail="Invalid token")
    return token


def get_or_create_user_state(token: str) -> UserEnvState:
    state = USER_ENVS.get(token)
    if state is None:
        env = gym.make(ENV_ID)
        state = UserEnvState(env=env)
        USER_ENVS[token] = state
    state.last_seen = time.time()
    return state


# ----------------- App -----------------
app = FastAPI(title="Hackathon Gym Env Server", version="1.0")


@app.on_event("startup")
async def startup() -> None:
    # Nettoyage périodique des envs inactifs
    async def reaper() -> None:
        while True:
            now = time.time()
            to_delete = []
            for token, state in list(USER_ENVS.items()):
                if now - state.last_seen > SESSION_TTL_SECONDS:
                    to_delete.append(token)

            for token in to_delete:
                state = USER_ENVS.pop(token, None)
                if state is not None:
                    # fermer l'env en thread, au cas où
                    await anyio.to_thread.run_sync(state.env.close)

            await anyio.sleep(30)  # cadence du nettoyage

    app.state.reaper_task = anyio.create_task_group()
    await app.state.reaper_task.__aenter__()
    app.state.reaper_task.start_soon(reaper)


@app.on_event("shutdown")
async def shutdown() -> None:
    # Stop reaper
    tg = getattr(app.state, "reaper_task", None)
    if tg is not None:
        await tg.__aexit__(None, None, None)

    # Fermer tous les envs
    for token, state in list(USER_ENVS.items()):
        try:
            await anyio.to_thread.run_sync(state.env.close)
        except Exception:
            pass
    USER_ENVS.clear()


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"status": "ok", "active_users": len(USER_ENVS), "env_id": ENV_ID}


@app.post("/reset", response_model=ResetResponse)
async def reset(req: ResetRequest, token: str = Depends(get_token)) -> ResetResponse:
    state = get_or_create_user_state(token)

    async with state.lock:
        # reset en thread pour ne pas bloquer l'event loop
        obs, info = await anyio.to_thread.run_sync(
            lambda: state.env.reset(seed=req.seed, options=req.options)
        )
        state.step_count = 0
        state.last_seen = time.time()

    return ResetResponse(observation=obs, info=info if isinstance(info, dict) else {"info": str(info)})


@app.post("/step", response_model=StepResponse)
async def step(req: StepRequest, token: str = Depends(get_token)) -> StepResponse:
    state = get_or_create_user_state(token)

    async with state.lock:
        # validations (l'action_space existe après gym.make)
        if not state.env.action_space.contains(req.action):
            raise HTTPException(status_code=400, detail="Invalid action for this env")

        if state.step_count >= MAX_STEPS_PER_EPISODE:
            raise HTTPException(status_code=400, detail="Max steps per episode exceeded; call /reset")

        obs, reward, terminated, truncated, info = await anyio.to_thread.run_sync(
            lambda: state.env.step(req.action)
        )

        state.step_count += 1
        state.last_seen = time.time()

    return StepResponse(
        observation=obs,
        reward=float(reward),
        terminated=bool(terminated),
        truncated=bool(truncated),
        info=info if isinstance(info, dict) else {"info": str(info)},
        step_count=state.step_count,
    )
