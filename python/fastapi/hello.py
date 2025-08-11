# Run with: fastapi dev hello.py --port 8000
# then open http://localhost:8000/docs

import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def root() -> str:
    return "Hello, World!"