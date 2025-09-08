# main.py
import os
import logging
import discord
from discord.ext import commands
from flask import Flask, jsonify
from threading import Thread

from takkari_bot.utils.db import init_db, execute

# ---------------- 로그 설정 ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- Discord 설정 ----------------
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # 메시지 내용 접근

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- Flask 서버 ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "따까리봇이 실행 중입니다 🚀"

@app.route("/status")
def status():
    # DB 체크
    try:
        rows = execute("SELECT name FROM sqlite_master WHERE type='table';", fetch=True)
        db_status = f"{len(rows)} tables" if rows else "No tables"
    except Exception as e:
        db_status = f"Error: {e}"

    return jsonify({
        "bot": str(bot.user) if bot.user else "Not logged in",
        "guilds": len(bot.guilds) if bot.user else 0,
        "db_status": db_status,
        "status": "running ✅"
    })

def run_web():
    app.run(host="0.0.0.0", port=10000)

# ---------------- 이벤트 ----------------
@bot.event
async def on_ready():
    logger.info(f"✅ 로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="따까리봇 2.0 🚀"))

async def load_cogs():
    extensions = [
        "takkari_bot.cogs.help",
        "takkari_bot.cogs.schedule",
        "takkari_bot.cogs.patchnote",
        "takkari_bot.cogs.support",
        "takkari_bot.cogs.userinfo",
        "takkari_bot.cogs.db_lookup",
        "takkari_bot.cogs.loglookup",
        "takkari_bot.cogs.dm_feature",
        "takkari_bot.cogs.accordingtobot",
    ]

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Loaded extension: {ext}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {ext}: {e}")

@bot.event
async def setup_hook():
    bot.remove_command("help")  # 기존 help 제거
    await load_cogs()
    synced = await bot.tree.sync()
    logger.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료 (Global)")

# ---------------- 실행 ----------------
if __name__ == "__main__":
    # DB 초기화
    init_db()
    logger.info("✅ DB 초기화 완료")

    # Flask 실행
    t = Thread(target=run_web)
    t.start()

    # Discord 실행
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    bot.run(TOKEN)