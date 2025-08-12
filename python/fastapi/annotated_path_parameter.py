# Run with: fastapi dev annotated_path_parameter.py --port 8000
# then open http://localhost:8000/docs

from typing import Annotated
import fastapi

app = fastapi.FastAPI()

@app.get('/hello/{name}')
def foo(
    name : Annotated[str, fastapi.Path(max_length=10)],
    email : Annotated[str, fastapi.Path(pattern="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")]
) -> str:
    return f"Hello {name} {email}"