# Run with: fastapi dev deprecated_param.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from typing import Annotated

app = fastapi.FastAPI()

@app.get("/")
def foo(
    lastname : Annotated[str, fastapi.Query(deprecated=True)]
):
    print(lastname)