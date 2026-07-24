import os
from pathlib import Path

from fastapi import FastAPI

TOKEN_FILE = Path(os.environ.get("TOKEN_FILE", "/mnt/secrets/token"))

app = FastAPI()


@app.get("/")
def hello():
    # Read at every request, not at startup: when the CSI driver rotates the
    # secret it rewrites this file in place, so the new value is picked up
    # without restarting the Pod — which an environment variable cannot do.
    try:
        token = TOKEN_FILE.read_text().strip()
    except FileNotFoundError:
        token = "(not mounted)"

    return {
        "message": os.environ.get("MESSAGE", "hello"),
        "secret_token": token,
    }
