# Run with: fastapi dev param_literal.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from typing import Literal

app = fastapi.FastAPI()

@app.get('/hello/{name}')
def foo(name : Literal["Alice", "Charles", "Jean"]):
    if name is "Charles":
        return f"Bonjour {name}"
    elif name == "Alice":
        return f"Hi {name}"
    else:
        return f"Salut {name}"
