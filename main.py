import discord
from discord.ext import commands, tasks
from discord import app_commands
from flask import Flask
import asyncio
import logging
from takkari_bot.utils import logging_config

# ----------------- 로깅 설정 -----------------
logger = logging_config.setup_logging()

# ----------------- Discord Bot -----------------
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# 순환 Presence 메시지
status_messages = [
    "🔥 서버를 관리",
    "🚀 업데이트 준비",
    "🤖 AI로 코딩"
]

@tasks.loop(seconds=30)
async def change_status():
    await bot.wait_until_ready()
    for msg in status_messages:
        await bot.change_presence(activity=discord.Game(msg))
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    change_status.start()

# ----------------- Cogs 로드 -----------------
cogs = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.fun",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.accordingtobot"
]

for cog in cogs:
    try:
        bot.load_extension(cog)
        logger.info(f"✅ {cog} 로드 완료")
    except Exception as e:
        logger.error(f"❌ {cog} 로드 실패: {e}")

# ----------------- Flask 웹 서버 -----------------
app = Flask("takkari_bot")

@app.route("/")
def home():
    return "봇 서버가 정상 작동 중입니다! 💖"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ----------------- 메인 -----------------
if __name__ == "__main__":
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    bot.run("DISCORD_TOKEN")
