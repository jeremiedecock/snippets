# Run with: fastapi dev path_and_query_params_with_underscores_and_hyphen.py --port 8000
# then open http://localhost:8000/docs

import fastapi

app = fastapi.FastAPI()

@app.get('/hello/{last_name}')
def foo(
    last_name : str,
    user_title : str | None = None
    # user_title : str | None = fastapi.Query(default=None, alias="user-title")  # 👈 query parameter avec tiret
) -> str:
    # return f"Hello {last_name}"
    return f"Hello {user_title} {last_name}"