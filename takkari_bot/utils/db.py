import sqlite3
import os

# DB 파일 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "../../shared/user.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 사용자 테이블
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE,
        name TEXT,
        joined_at TEXT
    )
    """)

    # 패치노트
    c.execute("""
    CREATE TABLE IF NOT EXISTS patchnotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 고객지원
    c.execute("""
    CREATE TABLE IF NOT EXISTS support (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 예약 공지
    c.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        content TEXT,
        channel_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 즉시 공지 로그
    c.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        channel_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def get_supports():
    """support 테이블에서 고객지원 기록 가져오기"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, user, message, created_at FROM support ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows
