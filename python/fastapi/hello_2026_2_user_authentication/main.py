#!/usr/bin/env python3

# You can test this snippet with the following command: `curl -X 'GET' 'http://127.0.0.1:8000/api/hello' -H 'accept: application/json' -H 'Authorization: Bearer token_abc123'`

import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging


# Configure logging
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = fastapi.FastAPI(root_path="/api")


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

    return username


###############################################################################
# ENDPOINTS ###################################################################
###############################################################################

@app.get("/hello")
async def get_hello(
    username: str = Depends(verify_token)
) -> str:
    """
    Protected endpoint that returns a personalized greeting.
    Requires a valid Bearer token in the Authorization header.
    """
    return f"Hello {username}"
