#!/usr/bin/env python3

import fastapi
import logging
from .routers import users


# Configure logging
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = fastapi.FastAPI(root_path="/api")

# Include the users router
app.include_router(users.router)

# Retrieve the API version and other information
@app.get("/hello")
async def get_hello() -> str:
    return "Hello, World!"
