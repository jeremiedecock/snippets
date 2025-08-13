# Run with: fastapi dev after_validator.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from typing import Annotated
from pydantic import AfterValidator

app = fastapi.FastAPI()

def check_value(x: int):
    if x % 2 != 0:
        raise ValueError("Value must be even")
    return x

@app.get("/")
def foo(
    x : Annotated[int, AfterValidator(check_value)]
) -> int:
    return x