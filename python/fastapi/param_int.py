# Run with: fastapi dev param_str.py --port 8000
# then open http://localhost:8000/docs

import fastapi

app = fastapi.FastAPI()

@app.get('/square/{x}')
def foo(x : int) -> dict:
    return {"result": x ** 2}