import hello_sqlite_fixtures as hello
import pytest
import sqlite3
from sqlite3 import Connection
from typing import Generator


@pytest.fixture    # 👈
def db_connection() -> Generator[Connection, None, None]:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?)",
        [(1, "Alice"), (2, "Bob",), (3, "Charlie",)]
    )
    conn.commit()
    yield conn
    conn.close()


def test_get_user_by_id(db_connection: Connection) -> None:                # 👈 c'est le nom de la fonction fixture qu'on met ici (et son type de retour)
    assert hello.get_user_by_id(db_connection, user_id=1) == "Alice"


def test_get_user_by_id_invalid_id(db_connection: Connection) -> None:     # 👈 c'est le nom de la fonction fixture qu'on met ici (et son type de retour)
    hello.get_user_by_id(db_connection, user_id=-1) is None