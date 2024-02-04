from typing import Union

from fastapi import FastAPI

app = FastAPI(
    docs_url=None, # Disable docs (Swagger UI)
    redoc_url=None, # Disable redoc
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
