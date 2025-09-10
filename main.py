import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from takkari_bot.utils import logging_config

logger = logging_config.setup_logging()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, application_id=1411657882876907540)

# ----------------- 순환 Presence -----------------
status_messages = [
    "😢 개발자는 버그 수정",
    "🚀 업데이트 준비",
    "🔥 열심히 일"
]
current_status = 0

@tasks.loop(seconds=15)
async def change_presence():
    global current_status
    await bot.change_presence(activity=discord.Game(name=status_messages[current_status]))
    current_status = (current_status + 1) % len(status_messages)

@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    change_presence.start()
    # 슬래시 커맨드 동기화
    try:
        await bot.tree.sync()
        logger.info(f"슬래시 커맨드 동기화됨: {len(bot.tree.walk_commands())}개")
    except Exception as e:
        logger.error(f"슬래시 커맨드 동기화 실패: {e}")

# ----------------- Cogs 로딩 -----------------
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

async def load_all_cogs():
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ {cog} 로드 완료")
        except Exception as e:
            logger.error(f"❌ {cog} 로드 실패: {e}")

asyncio.run(load_all_cogs())

# ----------------- 실행 -----------------
bot.run("YOUR_BOT_TOKEN")