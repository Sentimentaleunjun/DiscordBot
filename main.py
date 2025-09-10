import discord
from discord.ext import commands, tasks
import asyncio
import os
from takkari_bot.utils import db, logging_config

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
logger = logging_config.setup_logging()

status_messages = [
    "🔥 {servers}개의 서버에서 열일중!",
    "🚀 업데이트 준비중",
    "🤖 AI로 코딩중"
]

@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    change_status.start()
    try:
        synced = await bot.tree.sync()
        logger.info(f"슬래시 커맨드 동기화됨: {len(synced)}개")
    except Exception as e:
        logger.error(f"슬래시 커맨드 동기화 실패: {e}")

@tasks.loop(seconds=10)
async def change_status():
    guild_count = len(bot.guilds)
    msg = status_messages[change_status.current_loop % len(status_messages)].format(servers=guild_count)
    await bot.change_presence(activity=discord.Game(name=msg))

async def load_cogs():
    for folder in os.listdir("takkari_bot/cogs"):
        if folder.endswith(".py"):
            try:
                await bot.load_extension(f"takkari_bot.cogs.{folder[:-3]}")
                logger.info(f"✅ {folder} 로드 성공")
            except Exception as e:
                logger.error(f"❌ {folder} 로드 실패: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())