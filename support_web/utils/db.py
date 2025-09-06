import sqlite3
from datetime import datetime

DB_PATH = "support.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            status TEXT DEFAULT 'open',
            created_at TEXT
        )
        """)
        conn.commit()

def add_support(user_id, message):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO supports (user_id, message, status, created_at)
        VALUES (?, ?, 'open', ?)
        """, (user_id, message, datetime.utcnow().isoformat()))
        conn.commit()

def get_supports():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, message, status, created_at FROM supports ORDER BY id DESC")
        return cur.fetchall()

def close_support(support_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE supports SET status = 'closed' WHERE id = ?", (support_id,))
        conn.commit()
        return cur.rowcount > 0
