#!/usr/bin/env python3
"""
Demonstration of shared state in FastAPI without a database.

This example shows how to maintain state in memory between HTTP requests
using a CounterManager that provides one counter per authenticated user.

Each user (identified by their Bearer token) has their own isolated counter.
Asyncio locks are used to ensure thread-safety for concurrent requests.

Note: This is for demonstration purposes only. In production, consider using
a proper database or cache (Redis, etc.) for persistence and scalability.
"""

import asyncio
import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging


# Configure logging
logger = logging.getLogger(__name__)


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

class UserCounter:
    """
    Thread-safe counter class to demonstrate shared state.

    One instance is created per authenticated user and is accessed
    across multiple HTTP requests for that user.
    Uses an asyncio.Lock to ensure safe concurrent access.

    Attributes
    ----------
    value : int
        The current counter value.
    """

    def __init__(self):
        """Initialize the counter with value 0 and create the async lock."""
        self.value = 0
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        """Increment the counter and return the new value."""
        async with self._lock:
            self.value += 1
            return self.value

    async def get(self) -> int:
        """Return the current counter value."""
        # Remark: Locking here is optional since reading an int is atomic
        return self.value

    async def reset(self) -> None:
        """Reset the counter to zero."""
        async with self._lock:
            self.value = 0


class CounterManager:
    """
    Manager for user counters.

    This class handles:
    - One counter per authenticated token
    - Thread-safe access via a global lock for counter creation/deletion
    - Each UserCounter has its own lock for value operations

    Note: Counters persist in memory until explicitly removed or server restart.
    Consider implementing TTL-based cleanup for production use.
    """

    def __init__(self):
        self._counters: dict[str, UserCounter] = {}
        self._global_lock = asyncio.Lock()

    async def get_or_create_counter(self, token: str) -> UserCounter:
        """
        Get the counter for a token, creating it if necessary.

        Parameters
        ----------
        token : str
            The authentication token.

        Returns
        -------
        UserCounter
            The counter state for this token.
        """
        # Fast path: counter already exists, no lock needed
        if token in self._counters:
            return self._counters[token]

        # Slow path: need to create, acquire global lock
        async with self._global_lock:
            # Double-check after acquiring lock
            if token not in self._counters:
                self._counters[token] = UserCounter()
            return self._counters[token]

    async def remove_counter(self, token: str) -> None:
        """
        Remove and close an counter for a token.

        Parameters
        ----------
        token : str
            The authentication token.
        """
        async with self._global_lock:
            if token in self._counters:
                username = VALID_TOKENS.get(token, "unknown")
                del self._counters[token]
                logger.debug(f"Removed counter for user: {username}")

    async def get_active_count(self) -> int:
        """
        Return the number of active counters.

        Returns
        -------
        int
            The number of currently active user counters.
        """
        async with self._global_lock:
            return len(self._counters)


# Global counter manager instance
counter_manager = CounterManager()


###############################################################################
# LIFESPAN AND APP CREATION ###################################################
###############################################################################

# Create the FastAPI app
app = fastapi.FastAPI(root_path="/api")


###############################################################################
# API ENDPOINTS ###############################################################
###############################################################################

@app.get("/counter")
async def get_counter(
    token: str = Depends(verify_token)
) -> dict[str, int]:
    """Get the current counter value."""
    counter = await counter_manager.get_or_create_counter(token)
    return {"value": await counter.get()}


@app.post("/counter/increment")
async def increment_counter(
    token: str = Depends(verify_token)
) -> dict[str, int]:
    """Increment the counter and return the new value."""
    counter = await counter_manager.get_or_create_counter(token)
    new_value = await counter.increment()
    return {"value": new_value}


@app.post("/counter/reset")
async def reset_counter(
    token: str = Depends(verify_token)
) -> dict[str, int]:
    """Reset the counter to zero."""
    counter = await counter_manager.get_or_create_counter(token)
    await counter.reset()
    return {"value": await counter.get()}
