import discord
from discord.ext import commands, tasks
import asyncio
import os
from itertools import cycle
from takkari_bot.utils.logging_config import setup_logging

# -------------------- 로그 설정 --------------------
logger = setup_logging()

# -------------------- 봇 설정 --------------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# -------------------- 코그 목록 --------------------
COGS = [
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

# -------------------- 상태 메시지 --------------------
status_messages = cycle([
    lambda: f"{len(bot.guilds)}개의 서버 관리중 🔥",
    lambda: "업데이트 준비중 🚀",
    lambda: "🤖 AI로 코딩중"
])

@tasks.loop(seconds=20)
async def change_presence():
    msg = next(status_messages)()
    await bot.change_presence(activity=discord.Game(name=msg))

# -------------------- 코그 로드 --------------------
@bot.event
async def on_ready():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ {cog} 로드 완료")
        except Exception as e:
            logger.error(f"❌ {cog} 로드 실패: {e}")
    change_presence.start()
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")

# -------------------- 봇 실행 --------------------
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)
