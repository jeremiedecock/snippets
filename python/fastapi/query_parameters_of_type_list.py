# Run with: fastapi dev query_parameters_of_type_list.py --port 8000
# then open http://localhost:8000/docs

from typing import Annotated
import fastapi

app = fastapi.FastAPI()

@app.get('/hello/')
def foo(
    name : Annotated[list[str] | None, fastapi.Query()] = None
) -> str:
    return "Hello " + ",".join(name) if name is not None else ""