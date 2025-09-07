import sqlite3
from datetime import datetime

DB_PATH = "shared/user.db"

def execute(query, params=(), fetch=False, commit=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    result = c.fetchall() if fetch else None
    if commit:
        conn.commit()
    conn.close()
    return result

# ---------- DB 초기화 ----------
def init_db():
    execute("""
    CREATE TABLE IF NOT EXISTS dm_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """, commit=True)

    execute("""
    CREATE TABLE IF NOT EXISTS support (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        closed_at DATETIME
    )
    """, commit=True)

    execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """, commit=True)

# ---------- DM ----------
def add_dm(sender_id, receiver_id, message):
    execute(
        "INSERT INTO dm_logs (sender_id, receiver_id, message) VALUES (?, ?, ?)",
        (sender_id, receiver_id, message),
        commit=True
    )

# ---------- Support ----------
def add_support(user_id, message):
    execute(
        "INSERT INTO support (user_id, message) VALUES (?, ?)",
        (user_id, message),
        commit=True
    )

def get_supports():
    return execute(
        "SELECT id, user_id, message, status, created_at FROM support",
        fetch=True
    )

def close_support(support_id):
    row = execute(
        "SELECT user_id FROM support WHERE id=? AND status='open'",
        (support_id,),
        fetch=True
    )
    if not row:
        return None
    user_id = row[0][0]
    execute(
        "UPDATE support SET status='closed', closed_at=? WHERE id=?",
        (datetime.now(), support_id),
        commit=True
    )
    return user_id

# ---------- Schedule ----------
def add_schedule(content):
    execute("INSERT INTO schedules (content) VALUES (?)", (content,), commit=True)

def get_schedules():
    return execute("SELECT id, content, created_at FROM schedules", fetch=True)

def remove_schedule(schedule_id):
    execute("DELETE FROM schedules WHERE id=?", (schedule_id,), commit=True)
