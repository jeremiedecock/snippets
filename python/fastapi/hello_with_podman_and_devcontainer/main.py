#!/usr/bin/env python3

import fastapi
import logging


# Configure logging
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = fastapi.FastAPI(root_path="/api")


# Retrieve the API version and other information
@app.get("/hello")
async def get_hello() -> str:
    return "Hello, World!"
