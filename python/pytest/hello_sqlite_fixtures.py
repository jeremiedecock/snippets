import sqlite3

def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> str | None:
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return row[1] if row else None
