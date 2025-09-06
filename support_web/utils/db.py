import sqlite3

DB_PATH = "support.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_support(user_id: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO support_requests (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()

def get_supports():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = None  # ⚡ 튜플로 반환 고정
    c = conn.cursor()
    c.execute("SELECT id, user_id, message, created_at FROM support_requests ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows
