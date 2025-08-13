# Run with: fastapi dev get_header.py --port 8000
# then open http://localhost:8000/docs

from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}