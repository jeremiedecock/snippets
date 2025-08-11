# Run with: fastapi dev path_and_query_params2.py --port 8000
# then open http://localhost:8000/docs

import fastapi

app = fastapi.FastAPI()

@app.get('/hello/{lastname}/{firsname}')
def foo(
    firstname : str,
    lastname : str,
    title : str | None = None
) -> str:
    if title is None:
        return f"Hello {firstname} {lastname}"
    else:
        return f"Hello {title} {firstname} {lastname}"