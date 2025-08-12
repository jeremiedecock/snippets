# Run with: fastapi dev annotated_query_parameter.py --port 8000
# then open http://localhost:8000/docs

from typing import Annotated
import fastapi

app = fastapi.FastAPI()

@app.get('/hello/')
def foo(
    name : Annotated[str, fastapi.Query(max_length=10)]
) -> str:
    return f"Hello {name}"