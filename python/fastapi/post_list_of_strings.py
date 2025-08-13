# Run with: fastapi dev post_list_of_strings.py --port 8000
# then open http://localhost:8000/docs

import fastapi
from typing import Annotated

app = fastapi.FastAPI()

@app.post('/')
def foo(
    name : Annotated[list[str], fastapi.Query()]                         # 👈 
):
    print(name)