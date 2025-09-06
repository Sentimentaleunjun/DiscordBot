import os
import sys
import pathlib
import logging
import discord
from discord.ext import commands

# ===== 설정 =====
TOKEN = os.getenv("DISCORD_TOKEN") or "PUT_YOUR_TOKEN_HERE"   # 환경변수 권장
GUILD_ID = int(os.getenv("GUILD_ID", "0")) or None            # 빠른(길드) 동기화용. 없으면 전역 동기화

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # 파일들이 다른 경로에 있어도 import 가능하게

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 코그는 takkari_bot/cogs/ 안에 있으므로 전체 경로 지정
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
            logging.info("✅ Guild slash commands synced for %s", GUILD_ID)
        else:
            await bot.tree.sync()
            logging.info("✅ Global slash commands synced")
    except Exception as e:
        logging.exception("❌ Slash command sync failed: %s", e)

@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run(TOKEN)
