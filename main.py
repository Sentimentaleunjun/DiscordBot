import os
import logging
import asyncio
from itertools import cycle

import discord
from discord.ext import commands, tasks
from discord import app_commands

from flask import Flask
from threading import Thread

# ---------------------------
# 로깅 설정
# ---------------------------
logging.basicConfig(level=logging.INFO)

# ---------------------------
# Discord 봇 설정
# ---------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 상태 메시지 로테이션
statuses = cycle([
    "GSEJ Company 서비스 중",
    "새로운 기능 업데이트 확인",
    "따까리봇 도움 필요해?"
])

@tasks.loop(seconds=20)
async def cycle_status():
    await bot.change_presence(activity=discord.Game(next(statuses)))

# ---------------------------
# Flask 웹 서버
# ---------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "따까리봇 Web Service Running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ---------------------------
# 봇 이벤트
# ---------------------------
@bot.event
async def on_ready():
    logging.info(f"🤖 Logged in as {bot.user} ({bot.user.id})")

    # Cog 로드
    initial_extensions = [
        "takkari_bot.cogs.helpcmd",
        "takkari_bot.cogs.schedule",
        "takkari_bot.cogs.patchnote",
        "takkari_bot.cogs.support",
        "takkari_bot.cogs.userinfo",
        "takkari_bot.cogs.db_lookup",
        "takkari_bot.cogs.loglookup",
        "takkari_bot.cogs.announce",
    ]

    for ext in initial_extensions:
        try:
            bot.load_extension(ext)
            logging.info(f"✅ Loaded extension: {ext}")
        except Exception as e:
            logging.error(f"❌ Failed to load extension {ext}: {e}")

    # 명령어 동기화
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료")
    except Exception as e:
        logging.error(f"명령어 동기화 실패: {e}")

    # 상태 로테이션 시작
    if not cycle_status.is_running():
        cycle_status.start()

# ---------------------------
# 실행부
# ---------------------------
if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ["DISCORD_TOKEN"])
