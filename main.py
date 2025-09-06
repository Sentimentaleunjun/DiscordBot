import os
import sys
import pathlib
import logging
import asyncio
import discord
from discord.ext import commands
from itertools import cycle

# ===== 설정 =====
TOKEN = os.getenv("DISCORD_TOKEN") or "PUT_YOUR_TOKEN_HERE"
GUILD_ID = int(os.getenv("GUILD_ID", "0")) or None

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 상태 메시지 (커스텀)
status_list = cycle([
    "문의 접수 대기중 📨",
    "일정 관리중 ⏰",
    "따까리봇 정식 서비스 업데이트 고민중 🚀"
])

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
            logging.info("✅ Guild slash commands synced")
        else:
            await bot.tree.sync()
            logging.info("✅ Global slash commands synced")
    except Exception as e:
        logging.exception("❌ Slash command sync failed: %s", e)

async def cycle_status():
    while True:
        await bot.change_presence(
            activity=discord.CustomActivity(name=next(status_list)),
            status=discord.Status.online
        )
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)
    bot.loop.create_task(cycle_status())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run(TOKEN)
