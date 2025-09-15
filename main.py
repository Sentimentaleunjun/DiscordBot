# main.py
import discord
from discord.ext import commands
import asyncio
import logging
from flask import Flask
import threading
import os
import sqlite3

# -----------------------------
# 환경변수
TOKEN = os.environ.get("DISCORD_TOKEN")
LOG_CHANNEL_ID = 1417052732019310652
PORT = 10000
DB_PATH = "db.sqlite"

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
# Discord 로그 핸들러
class DiscordLogHandler(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id
        self.queue = asyncio.Queue()
        # bot이 준비된 후 로그 워커 실행
        asyncio.create_task(self.start_worker())

    async def start_worker(self):
        await self.bot.wait_until_ready()
        asyncio.create_task(self.log_worker())

    async def log_worker(self):
        channel = self.bot.get_channel(self.channel_id)
        while True:
            log_entry = await self.queue.get()
            try:
                if channel:
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

# Discord 로그 채널 핸들러 연결
discord_handler = DiscordLogHandler(bot, LOG_CHANNEL_ID)
discord_handler.setFormatter(formatter)
logger.addHandler(discord_handler)

# -----------------------------
# DB 초기화
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
        "takkari_bot.cogs.help",
        "takkari_bot.cogs.patchnote",
        "takkari_bot.cogs.db_lookup",
        "takkari_bot.cogs.",
        "takkari_bot.cogs.riot"
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
    init_db()
    await load_cogs()
    threading.Thread(target=run_flask, daemon=True).start()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())