import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": os.environ.get("MESSAGE", "hello")}
