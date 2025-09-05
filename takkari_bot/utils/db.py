import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../shared/user.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ?ъ슜???뚯씠釉?
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id TEXT UNIQUE,
        name TEXT,
        joined_at TEXT
    )
    """)

    # ?⑥튂?명듃
    c.execute("""
    CREATE TABLE IF NOT EXISTS patchnotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 怨좉컼吏??
    c.execute("""
    CREATE TABLE IF NOT EXISTS support (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ?덉빟 怨듭?
    c.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        content TEXT,
        channel_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 利됱떆 怨듭? 濡쒓렇
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
