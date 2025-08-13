# Run with: fastapi dev path_and_query_params_with_underscores_and_hyphen_via_alias.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from typing import Annotated

app = fastapi.FastAPI()

@app.get("/")
def foo(
    last_name : Annotated[str, fastapi.Query(alias="last-name")]  # 👈 query parameter avec tiret
) -> str:
    return f"Hello {last_name}"