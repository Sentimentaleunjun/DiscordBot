import sqlite3
import threading

DB_PATH = "shared/user.db"
_lock = threading.Lock()

def execute(sql, params=(), fetch=False, commit=False):
    with _lock:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            result = cur.fetchall() if fetch else None
            if commit:
                conn.commit()
        finally:
            cur.close()
            conn.close()
        return result

# Support
def init_support_table():
    execute("""
        CREATE TABLE IF NOT EXISTS support (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """, commit=True)

def add_support(user_id, message):
    execute("INSERT INTO support (user_id, message) VALUES (?, ?)", (user_id, message), commit=True)

def get_supports():
    return execute("SELECT id, user_id, message, status, created_at FROM support", fetch=True)

def close_support(support_id):
    if execute("SELECT id FROM support WHERE id=? AND status='open'", (support_id,), fetch=True):
        execute("UPDATE support SET status='closed' WHERE id=?", (support_id,), commit=True)
        return True
    return False

# Schedule
def init_schedule_table():
    execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """, commit=True)

def add_schedule(title, description, date):
    execute("INSERT INTO schedule (title, description, date) VALUES (?, ?, ?)", (title, description, date), commit=True)

def get_schedules():
    return execute("SELECT id, title, description, date FROM schedule", fetch=True)

# Init all tables
def init_db():
    init_support_table()
    init_schedule_table()
