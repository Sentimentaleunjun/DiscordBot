import os
import asyncio
import itertools
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
import threading

from takkari_bot.utils import db, logging_config

# ---------------- 로깅 ----------------
logger = logging_config.setup_logging()

# ---------------- Flask 서버 ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "TakkariBot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ---------------- Discord Bot 설정 ----------------
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Presence 메시지 (플레이 중만)
status_messages = itertools.cycle([
    lambda bot: discord.Game(f"✨ {len(bot.guilds)}개의 서버 지키는 중"),
    lambda bot: discord.Game("🍀 오늘도 행운 가득!"),
    lambda bot: discord.Game("🐣 아침엔 치킨 대신 코딩!"),
    lambda bot: discord.Game("🎉 따까리봇 1.0.1 출시 기념!"),
    lambda bot: discord.Game("💖 GSEJ Company 사랑해요!"),
    lambda bot: discord.Game("📅 일정 관리도 저한테 맡겨주세요!"),
    lambda bot: discord.Game("🤖 AI보다 귀여운 따까리봇"),
])

async def cycle_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        status = next(status_messages)(bot)
        await bot.change_presence(activity=status)
        await asyncio.sleep(10)

# ---------------- 이벤트 ----------------
@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        logger.info(f"슬래시 커맨드 동기화됨: {len(synced)}개")
    except Exception as e:
        logger.error(f"명령어 동기화 실패: {e}")

    bot.loop.create_task(cycle_status())

# ---------------- Cogs 로드 ----------------
async def load_cogs():
    cogs = [
        "userinfo",
        "support",
        "schedule",
        "patchnote",
        "loglookup",
        "help",
        "fun",
        "dm_feature",
        "db_lookup",
        "accordingtobot",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(f"takkari_bot.cogs.{cog}")
            logger.info(f"✅ {cog}.py 로드 성공")
        except Exception as e:
            logger.error(f"❌ {cog}.py 로드 실패: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    db.init_db()
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
