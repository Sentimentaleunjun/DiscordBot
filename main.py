# main.py
import os
import sys
import pathlib
import logging
import threading
import asyncio
import discord
from discord.ext import commands

from flask import Flask

# ===== 기본 설정 =====
TOKEN = os.getenv("DISCORD_TOKEN") or "PUT_YOUR_TOKEN_HERE"
GUILD_ID = int(os.getenv("GUILD_ID", "0")) or None

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

intents = discord.Intents.default()
intents.members = True  # 유저 관련 기능
bot = commands.Bot(command_prefix="!", intents=intents)  # 접두사는 남기되 / 중심

EXTENSIONS = [
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

# ===== Flask 웹 서버 (Render 포트 감시) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Takkari Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ===== 봇 상태 (Presence) =====
STATUS_MESSAGES = [
    "서버 관리 중",
    "GSEJ Company 서비스 운영",
    "문의는 /support 로!"
]

async def cycle_status():
    while True:
        for status in STATUS_MESSAGES:
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(30)  # 30초마다 상태 변경

# ===== Discord 이벤트 =====
@bot.event
async def setup_hook():
    # 코그 로드
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            logging.info("✅ Loaded extension: %s", ext)
        except Exception as e:
            logging.exception("❌ Failed to load extension %s: %s", ext, e)

    # 슬래시 명령어 동기화
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            synced = await bot.tree.sync(guild=guild)
            logging.info("✅ %d 개의 슬래시 명령어 동기화 완료 (Guild)", len(synced))
        else:
            synced = await bot.tree.sync()
            logging.info("✅ %d 개의 슬래시 명령어 동기화 완료 (Global)", len(synced))
    except Exception as e:
        logging.exception("❌ Slash command sync failed: %s", e)

@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)
    bot.loop.create_task(cycle_status())  # 상태 메시지 순환 시작

# ===== 실행부 =====
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=run_web, daemon=True).start()  # 웹 서버 실행
    bot.run(TOKEN)
