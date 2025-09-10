# main.py
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from flask import Flask
import threading
import os

from takkari_bot.utils.logging_config import setup_logging
from takkari_bot.utils import db

# -------------------- Logging --------------------
logger = setup_logging()

# -------------------- Bot Setup --------------------
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# -------------------- Presence Messages --------------------
status_messages = [
    "🔥 {guild_count}개의 서버에서 활동중!",
    "🚀 따까리봇 1.0.1 업데이트 완료!",
    "🤖 아재개그와 출석 체크 준비 완료!"
]

@tasks.loop(seconds=15)
async def rotate_presence():
    guild_count = len(bot.guilds)
    for msg in status_messages:
        await bot.change_presence(activity=discord.Game(msg.format(guild_count=guild_count)))
        await asyncio.sleep(15)

# -------------------- Cogs Loader --------------------
async def load_cogs():
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
        "takkari_bot.cogs.accordingtobot",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ {cog} 로드 완료")
        except Exception as e:
            logger.error(f"❌ {cog} 로드 실패: {e}")

# -------------------- Bot Events --------------------
@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()
    logger.info(f"슬래시 커맨드 동기화됨: {len(bot.tree.get_commands())}개")
    rotate_presence.start()

# -------------------- Flask App --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "따까리봇이 정상적으로 실행중입니다! 💖"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# -------------------- Main --------------------
if __name__ == "__main__":
    db.init_db()  # DB 초기화
    threading.Thread(target=run_flask).start()
    asyncio.run(load_cogs())
    bot.run(os.environ.get("DISCORD_TOKEN"))
