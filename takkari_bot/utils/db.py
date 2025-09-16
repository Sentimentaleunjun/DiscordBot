# takkari_bot/utils/db.py
import sqlite3
import threading
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../shared/user.db")
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

# -----------------------------
# Support 테이블
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

# -----------------------------
# Schedule 테이블
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

# -----------------------------
# Patchnote 테이블
def init_patchnote_table():
    execute("""
        CREATE TABLE IF NOT EXISTS patchnote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """, commit=True)

def add_patchnote(title, content, author_id):
    execute("INSERT INTO patchnote (title, content, author_id) VALUES (?, ?, ?)", (title, content, author_id), commit=True)

def get_patchnotes():
    return execute("SELECT id, title, content, author_id, created_at FROM patchnote ORDER BY created_at DESC", fetch=True)

# -----------------------------
# 모든 테이블 초기화
def init_db():
    init_support_table()
    init_schedule_table()
    init_patchnote_table()