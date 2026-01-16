#!/usr/bin/env python3
"""
Demonstration of shared state in FastAPI without a database.

This example shows how to maintain state in memory between HTTP requests
using a CounterManager that provides one counter per authenticated user.

Each user (identified by their Bearer token) has their own isolated counter.
anyio locks are used to ensure thread-safety for concurrent requests.

Note: This is for demonstration purposes only. In production, consider using
a proper database or cache (Redis, etc.) for persistence and scalability.
"""

import anyio
from contextlib import asynccontextmanager
import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import gymnasium as gym
import logging
import pydantic
from typing import Annotated, Any


# Configure logging
logger = logging.getLogger(__name__)


###############################################################################
# RL ENVIRONMENT CONFIGURATION ################################################
###############################################################################

# Default Gymnasium environment
DEFAULT_ENV_ID = "MountainCar-v0"

# Maximum steps per episode (to prevent infinite loops)
MAX_STEPS_PER_EPISODE = 1000


###############################################################################
# AUTHENTICATION ##############################################################
###############################################################################

# Security scheme for Bearer token authentication
security = HTTPBearer()

# Dictionary of valid tokens mapped to usernames
VALID_TOKENS = {
    "token_abc123": "alice",
    "token_def456": "bob",
    "token_ghi789": "charlie",
}

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify the Bearer token from the Authorization header.

    Parameters
    ----------
    credentials : HTTPAuthorizationCredentials
        The credentials extracted from the Authorization header.

    Returns
    -------
    str
        The verified token.

    Raises
    ------
    HTTPException
        401 if the token is invalid or not provided.
    """
    token = credentials.credentials

    if token not in VALID_TOKENS:
        logger.warning("Invalid token attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = VALID_TOKENS[token]
    logger.debug(f"Authenticated user: {username}")

    return token


###############################################################################
# STATE MANAGER ###############################################################
###############################################################################

class UserEnvironment:
    """
    State container for a single user's environment.

    One instance is created per authenticated user and is accessed
    across multiple HTTP requests for that user.
    Uses an anyio.Lock to ensure safe concurrent access.

    Attributes
    ----------
    env : gym.Env
        The Gymnasium environment instance.
    step_count : int
        Number of steps taken in the current episode.
    last_access : float
        Timestamp of last access (for TTL management).
    lock : anyio.Lock
        Per-user lock for serializing step/reset calls.
    """

    def __init__(self, env: gym.Env):
        self.env = env
        self.step_count = 0
        self._lock = anyio.Lock()


class EnvironmentManager:
    """
    Manager for user environments.

    This class handles:
    - One environment per token
    - Thread-safe access via per-token locks

    Note: Counters persist in memory until explicitly removed or server restart.
    """

    def __init__(self, env_id: str):
        self.env_id = env_id
        self._environments: dict[str, UserEnvironment] = {}
        self._global_lock = anyio.Lock()

    async def get_or_create_env(self, token: str) -> UserEnvironment:
        """
        Get the environment for a token, creating it if necessary.

        Parameters
        ----------
        token : str
            The authentication token.

        Returns
        -------
        UserEnvironment
            The environment state for this token.
        """
        # Fast path: counter already exists, no lock needed
        if token in self._environments:
            return self._environments[token]

        # Slow path: need to create, acquire global lock
        # TODO: create all environments at startup only (in the lifespan)?
        async with self._global_lock:
            # Double-check after acquiring lock
            if token not in self._environments:
                # Create environment in a thread to avoid blocking
                env = await anyio.to_thread.run_sync(
                    lambda: gym.make(self.env_id)
                )
                self._environments[token] = UserEnvironment(env)
            return self._environments[token]

    async def close_all(self) -> None:
        """Close all environments (for shutdown)."""
        async with self._global_lock:
            for token, env_state in list(self._environments.items()):
                await anyio.to_thread.run_sync(env_state.env.close)
            self._environments.clear()
            logger.info("All environments closed.")


# Global environment manager instance
env_manager = EnvironmentManager(DEFAULT_ENV_ID)


###############################################################################
# LIFESPAN AND APP CREATION ###################################################
###############################################################################

# Create Database and Tables on startup
# C.f. https://fastapi.tiangolo.com/advanced/events/#async-context-manager
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    yield

    # On shutdown, close all environments
    await env_manager.close_all()

# Create the FastAPI app
app = fastapi.FastAPI(lifespan=lifespan, root_path="/api")


###############################################################################
# RL PYDANTIC MODELS ##########################################################
###############################################################################

class ResetResponse(pydantic.BaseModel):
    """Response model for reset endpoint."""
    observation: Any
    info: dict[str, Any]

# class StepRequest(pydantic.BaseModel):
#     """Request model for stepping through an environment."""
#     action: Annotated[int, pydantic.Field(ge=0, le=1)]

class StepResponse(pydantic.BaseModel):
    """Response model for step endpoint."""
    observation: Any
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, Any]
    step_count: int


###############################################################################
# API ENDPOINTS ###############################################################
###############################################################################

@app.post("/reset")
async def reset_environment(
    token: str = Depends(verify_token)
) -> ResetResponse:
    """
    Reset the environment for the authenticated user.

    Parameters
    ----------
    token : str
        The authenticated user's token.

    Returns
    -------
    ResetResponse
        The initial observation and info from the environment.

    Raises
    ------
    HTTPException
        500 if an error occurs during reset.
    """
    user_environment = await env_manager.get_or_create_env(token)

    async with user_environment._lock:
        try:
            # Run reset in a thread to avoid blocking the event loop
            def do_reset():
                return user_environment.env.reset()

            observation, info = await anyio.to_thread.run_sync(do_reset)

            # Reset step counter
            user_environment.step_count = 0

            # Convert numpy arrays to lists for JSON serialization
            if hasattr(observation, "tolist"):
                observation = observation.tolist()

            return ResetResponse(observation=observation, info=info)

        except Exception as e:
            logger.error(f"Error during reset for token {token[:8]}...: {e}")
            raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step")
async def step_environment(
    action: Annotated[int, pydantic.Field(ge=0, le=2)],   # https://gymnasium.farama.org/environments/classic_control/mountain_car/#action-space
    token: str = Depends(verify_token)
) -> StepResponse:
    """
    Execute one step in the environment for the authenticated user.

    Parameters
    ----------
    request : StepRequest
        The step request containing the action to take.
    token : str
        The authenticated user's token.

    Returns
    -------
    StepResponse
        The observation, reward, terminated, truncated, info, and step count.

    Raises
    ------
    HTTPException
        400 if the environment hasn't been reset yet.
        400 if the episode is already terminated/truncated.
        400 if the maximum steps per episode is reached.
        500 if an error occurs during step.
    """
    user_environment = await env_manager.get_or_create_env(token)

    async with user_environment._lock:
        # Check if we've exceeded max steps
        if user_environment.step_count >= MAX_STEPS_PER_EPISODE:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum steps per episode ({MAX_STEPS_PER_EPISODE}) reached. Please reset."
            )

        try:
            # Run step in a thread to avoid blocking the event loop
            def do_step():
                return user_environment.env.step(action)

            observation, reward, terminated, truncated, info = await anyio.to_thread.run_sync(do_step)

            # Increment step counter
            user_environment.step_count += 1

            # Convert numpy arrays to lists for JSON serialization
            if hasattr(observation, "tolist"):
                observation = observation.tolist()
            if hasattr(reward, "item"):
                reward = reward.item()

            return StepResponse(
                observation=observation,
                reward=float(reward),
                terminated=bool(terminated),
                truncated=bool(truncated),
                info=info,
                step_count=user_environment.step_count
            )

        except Exception as e:
            logger.error(f"Error during step for token {token[:8]}...: {e}")
            raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")
