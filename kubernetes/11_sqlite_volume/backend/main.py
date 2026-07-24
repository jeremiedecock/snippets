import os
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "/data/messages.db")

app = FastAPI()


class Message(BaseModel):
    message: str


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT)"
    )
    return connection


@app.get("/")
def read_message():
    connection = get_connection()
    row = connection.execute(
        "SELECT message FROM messages ORDER BY id DESC LIMIT 1"
    ).fetchone()
    connection.close()
    return {
        "message": row[0] if row else "(no message yet)",
        "served_by": os.environ.get("HOSTNAME", "?"),
    }


@app.post("/")
def write_message(msg: Message):
    connection = get_connection()
    connection.execute("INSERT INTO messages (message) VALUES (?)", (msg.message,))
    connection.commit()
    connection.close()
    return {"saved": msg.message, "served_by": os.environ.get("HOSTNAME", "?")}
