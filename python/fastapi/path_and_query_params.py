# Run with: fastapi dev path_and_query_params.py --port 8000
# then open http://localhost:8000/docs

import fastapi

app = fastapi.FastAPI()

@app.get('/hello/{name}')
def foo(name : str, surname : str) -> str:
    return f"Hello {surname} {name}"