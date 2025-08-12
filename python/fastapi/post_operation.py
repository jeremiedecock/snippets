# Run with: fastapi dev post_operation.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = fastapi.FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item