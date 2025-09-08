# main.py
import os
import logging
import asyncio
import discord
from discord.ext import commands
from flask import Flask

# -----------------------------
# Flask 서버 설정
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "TakkariBot is running! ✅"

# -----------------------------
# Discord 봇 설정
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# cogs 자동 로딩
async def load_cogs():
    for filename in os.listdir("takkari_bot/cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            extension = f"takkari_bot.cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                logger.info(f"✅ Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"❌ Failed to load extension {extension}: {e}")

@bot.event
async def on_ready():
    await bot.tree.sync()  # 슬래시 명령어 동기화
    logger.info(f"🤖 Logged in as {bot.user}")
    logger.info(f"✅ {len(bot.tree.get_commands())} 개의 슬래시 명령어 동기화 완료")

# -----------------------------
# 실행부
# -----------------------------
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    # Flask는 별도 쓰레드에서 실행
    from threading import Thread

    port = int(os.environ.get("PORT", 5000))  # Render는 기본적으로 $PORT 환경변수를 씀
    Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()

    # Discord 봇 실행
    asyncio.run(main())