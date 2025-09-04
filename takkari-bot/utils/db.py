import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../shared/user.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS patchnotes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS support (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, content TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def add_patchnote(content):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO patchnotes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def get_patchnotes(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT content, created FROM patchnotes ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_support(user_id, content):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO support (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()
    conn.close()

def get_support():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT user_id, content, created FROM support ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
