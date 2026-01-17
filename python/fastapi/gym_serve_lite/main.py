#!/usr/bin/env python3
"""
Demonstration of shared state in FastAPI without a database.

This script maintains state in memory between HTTP requests
using an EnvironmentManager that provides one UserEnvironment per authenticated user.

Each user (identified by their Bearer token) has their own isolated UserEnvironment.
anyio locks are used to ensure thread-safety for concurrent requests.

Note: This is for demonstration purposes only. In production, consider using
a proper database or cache (Redis, etc.) for persistence and scalability.
"""

import anyio
from contextlib import asynccontextmanager
import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import gymnasium as gym
import io
import logging
from PIL import Image
import pydantic
from typing import Annotated, Any


# Configure logging
logger = logging.getLogger(__name__)


###############################################################################
# RL ENVIRONMENT CONFIGURATION ################################################
###############################################################################

# Default Gymnasium environment
# DEFAULT_ENV_ID = "MountainCar-v0"
DEFAULT_ENV_ID = "FrozenLake-v1"

DISCRETE_ACTION_SPACE_START = 0
# DISCRETE_ACTION_SPACE_SIZE = 3  # MountainCar-v0 has 3 discrete actions: 0 (push left), 1 (no push), 2 (push right) https://gymnasium.farama.org/environments/classic_control/mountain_car/#action-space
DISCRETE_ACTION_SPACE_SIZE = 4  # FrozenLake-v1 has 4 discrete actions https://gymnasium.farama.org/environments/toy_text/frozen_lake/


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
# RL ENVIRONMENTS MANAGER #####################################################
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
    lock : anyio.Lock
        Per-user lock for serializing step/reset calls.
    """

    def __init__(self, env: gym.Env):
        self.env = env
        self.lock = anyio.Lock()


class EnvironmentManager:
    """
    Manager for user environments.

    This class handles:
    - One environment per token
    - Thread-safe access via per-token locks

    Note: user environments persist in memory until explicitly removed or server restart.
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
        # Fast path: user environment already exists, no lock needed
        if token in self._environments:
            return self._environments[token]

        # Slow path: need to create, acquire global lock
        # TODO: create all environments at startup only (in the lifespan)?
        async with self._global_lock:
            # Double-check after acquiring lock
            if token not in self._environments:
                # Create environment in a thread to avoid blocking
                # Use render_mode='rgb_array' to enable rendering to images
                env = await anyio.to_thread.run_sync(
                    lambda: gym.make(self.env_id, render_mode="rgb_array")
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

    async with user_environment.lock:
        try:
            # Run reset in a thread to avoid blocking the event loop
            def do_reset():
                return user_environment.env.reset()

            observation, info = await anyio.to_thread.run_sync(do_reset)

            # Convert numpy arrays to lists for JSON serialization
            if hasattr(observation, "tolist"):
                observation = observation.tolist()

            return ResetResponse(observation=observation, info=info)

        except Exception as e:
            logger.error(f"Error during reset for token {token[:8]}...: {e}")
            raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step")
async def step_environment(
    action: Annotated[int, pydantic.Field(ge=DISCRETE_ACTION_SPACE_START, lt=DISCRETE_ACTION_SPACE_SIZE)],
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

    async with user_environment.lock:
        try:
            # Run step in a thread to avoid blocking the event loop
            def do_step():
                return user_environment.env.step(action)

            observation, reward, terminated, truncated, info = await anyio.to_thread.run_sync(do_step)

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
            )

        except Exception as e:
            logger.error(f"Error during step for token {token[:8]}...: {e}")
            raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.get("/render")
async def render_environment(
    token: str = Depends(verify_token)
) -> Response:
    """
    Render the current state of the environment as a PNG image.

    Parameters
    ----------
    token : str
        The authenticated user's token.

    Returns
    -------
    Response
        A PNG image of the current environment state.

    Raises
    ------
    HTTPException
        500 if an error occurs during rendering.
    """
    user_environment = await env_manager.get_or_create_env(token)

    async with user_environment.lock:
        try:
            # Run render in a thread to avoid blocking the event loop
            def do_render():
                return user_environment.env.render()

            frame = await anyio.to_thread.run_sync(do_render)

            if frame is None:
                raise HTTPException(
                    status_code=400,
                    detail="Environment render mode does not support image output. "
                           "Make sure the environment was created with render_mode='rgb_array'."
                )

            # Convert numpy array to PNG image
            def encode_image(frame):
                img = Image.fromarray(frame)
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                return buffer.getvalue()

            image_bytes = await anyio.to_thread.run_sync(lambda: encode_image(frame))

            return Response(content=image_bytes, media_type="image/png")

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during render for token {token[:8]}...: {e}")
            raise HTTPException(status_code=500, detail=f"Render failed: {str(e)}")
