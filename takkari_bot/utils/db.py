# takkari_bot/utils/db.py
# -*- coding: utf-8 -*-
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
    """고객지원 요청을 DB에 저장"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO support_requests (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()

def get_supports():
    """저장된 모든 고객지원 요청 불러오기"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, user_id, message, created_at FROM support_requests ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows
