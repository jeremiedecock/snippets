#!/usr/bin/env python3
"""
Demonstration of shared state in FastAPI without a database.

This example shows how to maintain state in memory between HTTP requests
using a simple Counter class. The state is shared across all requests.

A lock is used to ensure thread-safety for concurrent requests.
"""

import asyncio
from contextlib import asynccontextmanager
import fastapi


###############################################################################
# STATE MANAGER ###############################################################
###############################################################################

class Counter:
    """
    Thread-safe counter class to demonstrate shared state.

    This instance will be created once and shared across all HTTP requests.
    Uses an asyncio.Lock to ensure safe concurrent access.
    """

    def __init__(self):
        self.value = 0
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        """Increment the counter and return the new value."""
        async with self._lock:
            self.value += 1
            return self.value

    async def get(self) -> int:
        """Return the current counter value."""
        async with self._lock:
            return self.value

    async def reset(self) -> None:
        """Reset the counter to zero."""
        async with self._lock:
            self.value = 0


# Global counter instance - shared across all requests
counter = Counter()


###############################################################################
# LIFESPAN AND APP CREATION ###################################################
###############################################################################

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """
    Application lifespan context manager.

    This is where you can initialize resources on startup and clean them up
    on shutdown. For this simple example, we just reset the counter.

    See: https://fastapi.tiangolo.com/advanced/events/#async-context-manager
    """
    # Startup: initialize state
    await counter.reset()
    yield
    # Shutdown: cleanup (nothing to do here for a simple counter)


# Create the FastAPI app
app = fastapi.FastAPI(lifespan=lifespan, root_path="/api")


###############################################################################
# API ENDPOINTS ###############################################################
###############################################################################

@app.get("/counter")
async def get_counter() -> dict:
    """Get the current counter value."""
    return {"value": await counter.get()}


@app.post("/counter/increment")
async def increment_counter() -> dict:
    """Increment the counter and return the new value."""
    new_value = await counter.increment()
    return {"value": new_value}


@app.post("/counter/reset")
async def reset_counter() -> dict:
    """Reset the counter to zero."""
    await counter.reset()
    return {"value": await counter.get()}
