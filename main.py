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
DEV_ID = 909360134566862878  # 개발자(너) 디스코드 ID

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # 다른 폴더 import 가능하게

# ===== Bot 설정 =====
intents = discord.Intents.default()
intents.message_content = True  # 관리자 전용 명령들 대응
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 로드할 Cog 목록 =====
EXTENSIONS = [
    "takkari_bot.cogs.accordingtobot",  # 공지
    "takkari_bot.cogs.db_lookup",       # DB 조회 (관리자 전용)
    "takkari_bot.cogs.loglookup",       # 로그 조회 (관리자 전용)
    "takkari_bot.cogs.patchnote",       # 패치노트
    "takkari_bot.cogs.schedule",        # 일정 관리
    "takkari_bot.cogs.support",         # 문의 기능
    "takkari_bot.cogs.userinfo",        # 유저 정보
    "takkari_bot.cogs.help",            # 봇 소개/가이드
]

# ===== Presence 상태 관리 =====
status_list = cycle([
    "문의 접수 대기중📨",
    "일정 관리중 ⏰",
    "따까리봇 정식 서비스 업데이트 고민중 🚀"
])

async def cycle_status():
    while True:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=next(status_list)  # ~~~만 보이게
            ),
            status=discord.Status.online
        )
        await asyncio.sleep(30)  # 30초마다 변경

# ===== 이벤트 =====
@bot.event
async def setup_hook():
    # Cog 로드
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            logging.info("✅ Loaded extension: %s", ext)
        except Exception as e:
            logging.exception("❌ Failed to load extension %s: %s", ext, e)

    # 슬래시 동기화
    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            await bot.tree.sync(guild=guild)
            logging.info("🔄 Guild slash sync OK (%s)", GUILD_ID)
        else:
            await bot.tree.sync()
            logging.info("🌍 Global slash sync OK")
    except Exception as e:
        logging.exception("❌ Slash command sync failed: %s", e)

@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)
    bot.loop.create_task(cycle_status())

# ===== 실행 =====
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run(TOKEN)
