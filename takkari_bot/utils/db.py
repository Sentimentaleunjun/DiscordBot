import sqlite3
import threading

DB_PATH = "shared/user.db"  # DB 경로
_lock = threading.Lock()

# ---------------- 기본 DB 실행 함수 ----------------
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

# ---------------- Support 관련 ----------------
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
    rows = execute("SELECT id, user_id, message, status, created_at FROM support", fetch=True)
    return rows

def close_support(support_id):
    row = execute("SELECT id FROM support WHERE id=? AND status='open'", (support_id,), fetch=True)
    if row:
        execute("UPDATE support SET status='closed' WHERE id=?", (support_id,), commit=True)
        return True
    return False

# ---------------- Points 관련 ----------------
def init_points_table():
    execute("""
        CREATE TABLE IF NOT EXISTS points (
            user_id INTEGER PRIMARY KEY,
            point INTEGER DEFAULT 0
        )
    """, commit=True)

def add_point(user_id, amount):
    current = execute("SELECT point FROM points WHERE user_id=?", (user_id,), fetch=True)
    if current:
        execute("UPDATE points SET point=point+? WHERE user_id=?", (amount, user_id), commit=True)
    else:
        execute("INSERT INTO points (user_id, point) VALUES (?, ?)", (user_id, amount), commit=True)

def get_point(user_id):
    res = execute("SELECT point FROM points WHERE user_id=?", (user_id,), fetch=True)
    return res[0][0] if res else 0

# ---------------- Quiz 관련 ----------------
def init_quiz_table():
    execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """, commit=True)

def add_quiz(question, answer):
    execute("INSERT INTO quiz (question, answer) VALUES (?, ?)", (question, answer), commit=True)

def get_random_quiz():
    res = execute("SELECT id, question, answer FROM quiz ORDER BY RANDOM() LIMIT 1", fetch=True)
    return res[0] if res else None

# ---------------- 초기화 ----------------
def init_db():
    """모든 테이블 초기화"""
    init_support_table()
    init_points_table()
    init_quiz_table()