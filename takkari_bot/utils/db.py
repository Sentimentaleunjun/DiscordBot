# takkari_bot/utils/db.py
# -*- coding: utf-8 -*-
import os
import sqlite3

# DB 경로 (환경 변수 우선, 없으면 현재 utils 폴더에 support.db 생성)
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "support.db"))

def init_db():
    """DB 및 테이블 초기화"""
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
    """고객지원 요청 저장"""
    init_db()  # 테이블 없으면 생성
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO support_requests (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()

def get_supports():
    """모든 고객지원 요청 조회 (최신순)"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict처럼 접근 가능
    rows = conn.execute(
        "SELECT id, user_id, message, created_at FROM support_requests ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
