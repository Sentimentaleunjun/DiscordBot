import sqlite3
import os

DB_PATH = "database/bot.db"

def init_db():
    # database 폴더가 없으면 생성
    os.makedirs("database", exist_ok=True)

    # DB 연결 (없으면 자동으로 새로 생성됨)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 고객지원 문의 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 패치노트 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patch_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
