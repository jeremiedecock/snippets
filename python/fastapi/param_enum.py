# Run with: fastapi dev param_enum.py --port 8000
# then open http://localhost:8000/docs

from enum import Enum
import fastapi

app = fastapi.FastAPI()

class Name(str, Enum):
    alice = "Alice"
    charles = "Charles"
    jean = "Jean"

@app.get('/hello/{name}')
def foo(name : Name):
    if name is Name.charles:
        return f"Bonjour {name.value}"
    elif name.value == "Alice":
        return f"Hi {name.value}"
    else:
        return f"Salut {name.value}"
