import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../shared/user.db")

def get_support_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS support (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, message TEXT)")
    cursor.execute("SELECT id, user, message FROM support")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "user": r[1], "message": r[2]} for r in rows]
