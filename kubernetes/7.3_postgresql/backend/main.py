import os

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI()


class Message(BaseModel):
    message: str


def get_connection():
    connection = psycopg.connect(DATABASE_URL)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, message TEXT)"
    )
    connection.commit()
    return connection


@app.get("/")
def read_message():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT message FROM messages ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return {
        "message": row[0] if row else "(no message yet)",
        "served_by": os.environ.get("HOSTNAME", "?"),
    }


@app.post("/")
def write_message(msg: Message):
    with get_connection() as connection:
        connection.execute("INSERT INTO messages (message) VALUES (%s)", (msg.message,))
    return {"saved": msg.message, "served_by": os.environ.get("HOSTNAME", "?")}
