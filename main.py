# takkari_bot/main.py
import os
import sys
import pathlib
import logging
import threading
from flask import Flask
import discord
from discord.ext import commands

# ===== 설정 =====
TOKEN = os.getenv("DISCORD_TOKEN") or "PUT_YOUR_TOKEN_HERE"
GUILD_ID = int(os.getenv("GUILD_ID", "0")) or None

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # import 경로 잡기

# ===== Flask 웹 서버 =====
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ 따까리봇 웹 대시보드: 정상 작동 중!"

def run_web():
    port = int(os.environ.get("PORT", 5000))  # Render 지정 포트
    app.run(host="0.0.0.0", port=port)

# ===== Discord Bot =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = [
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.userinfo",
]

@bot.event
async def setup_hook():
    # 코그 로드
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            logging.info("✅ Loaded extension: %s", ext)
        except Exception as e:
            logging.exception("❌ Failed to load extension %s: %s", ext, e)

    # 슬래시 명령 동기화
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            await bot.tree.sync(guild=guild)
            logging.info("✅ Guild slash commands synced: %s", GUILD_ID)
        else:
            await bot.tree.sync()
            logging.info("✅ Global slash commands synced")
    except Exception as e:
        logging.exception("❌ Slash command sync failed: %s", e)

@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)

# ===== 실행 =====
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 웹 서버 스레드 실행
    threading.Thread(target=run_web).start()

    # 디스코드 봇 실행
    bot.run(TOKEN)

