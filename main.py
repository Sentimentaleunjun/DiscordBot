# main.py
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import logging
from flask import Flask
import threading
import os

# -----------------------------
# 환경변수
TOKEN = os.environ.get("DISCORD_TOKEN")
LOG_CHANNEL_ID = 1417052732019310652
PORT = 10000
DB_PATH = "db.sqlite"  # DB 파일 경로

# -----------------------------
# Flask 서버
app = Flask(__name__)

@app.route("/")
def home():
    return "Takkari Bot Server is running!"

def run_flask():
    logger.info(f"Flask 서버 시작 (포트 {PORT})")
    app.run(host="0.0.0.0", port=PORT)

# -----------------------------
# Discord Bot 로그 핸들러
class DiscordLogHandler(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id
        self.queue = asyncio.Queue()
        asyncio.create_task(self.log_worker())

    async def log_worker(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        while True:
            log_entry = await self.queue.get()
            try:
                await channel.send(f"```{log_entry}```")
            except Exception as e:
                print("Log send error:", e)

    def emit(self, record):
        log_entry = self.format(record)
        self.queue.put_nowait(log_entry)

# -----------------------------
# 로깅 설정
logger = logging.getLogger('takkari_bot')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# -----------------------------
# Bot 초기화
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 디스코드 로그 채널 핸들러 연결
discord_handler = DiscordLogHandler(bot, LOG_CHANNEL_ID)
discord_handler.setFormatter(formatter)
logger.addHandler(discord_handler)

# -----------------------------
# DB 초기화
def init_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # DB 테이블 예시
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)
    conn.commit()
    conn.close()
    logger.info("✅ DB 초기화 완료")

# -----------------------------
# 코그 로딩
async def load_cogs():
    cogs = [
        "takkari_bot.cogs.userinfo",
        "takkari_bot.cogs.announce",
        "takkari_bot.cogs.dm_feature",
        "takkari_bot.cogs.support",
        # 추가 코그 넣기
        "takkari_bot.cogs.riot_callback"
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ {cog} 로드 완료")
        except Exception as e:
            logger.exception(f"❌ {cog} 로드 실패: {e}")

# -----------------------------
# 봇 이벤트
@bot.event
async def on_ready():
    logger.info(f"봇 시작 완료: {bot.user}")

# -----------------------------
# 메인 실행
async def main():
    # DB 초기화
    init_db()

    # 코그 로드
    await load_cogs()

    # Flask 서버를 스레드로 실행
    threading.Thread(target=run_flask, daemon=True).start()

    # 봇 시작
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())