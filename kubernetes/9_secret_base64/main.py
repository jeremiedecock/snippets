import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {
        "message": os.environ.get("MESSAGE", "hello"),
        "secret_token": os.environ.get("SECRET_TOKEN", "(not set)"),
    }
