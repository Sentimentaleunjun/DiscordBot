import discord
from discord.ext import commands, tasks
import asyncio
import os

# Intents 설정
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # 멤버 관련 기능 필요 시

# Bot 객체 생성
bot = commands.Bot(command_prefix='/', intents=intents)

# 순환할 Presence 메시지
status_messages = [
    "Server Making… 🔥",
    "정식출시 준비중🚀",
    "🤖AI로 코딩중"
]

# Presence 순환 Task
@tasks.loop(seconds=10)
async def change_status():
    guild_count = len(bot.guilds)
    server_status = f"{guild_count}개의 서버 관리중 🔥"
    for msg in status_messages:
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=f"{msg} | {server_status}")
        )
        await asyncio.sleep(10)

# Bot 준비 시
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} | Ready!")
    change_status.start()
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# 모든 코그 자동 로드
async def load_all_cogs():
    cogs = [
        "takkari_bot.userinfo",
        "takkari_bot.support",
        "takkari_bot.schedule",
        "takkari_bot.patchnote",
        "takkari_bot.loglookup",
        "takkari_bot.help",
        "takkari_bot.fun",
        "takkari_bot.dm_feature",
        "takkari_bot.db_lookup",
        "takkari_bot.accordingtobot"
    ]
    for ext in cogs:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded cog: {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

# 메인 실행
async def main():
    async with bot:
        await load_all_cogs()
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
        await bot.start(token)

# asyncio로 실행
asyncio.run(main())