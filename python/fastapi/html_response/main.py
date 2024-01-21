from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# See: https://fastapi.tiangolo.com/advanced/custom-response/#html-response

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Root</title>
        </head>
        <body>
            <h1>Hello from root</h1>
        </body>
    </html>
    """


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Items</title>
        </head>
        <body>
            <h1>Hello from items</h1>
        </body>
    </html>
    """
