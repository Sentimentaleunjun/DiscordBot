import os
import discord
from discord.ext import commands
from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = 909360134566862878

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# DB 초기화
init_db()

@bot.event
async def on_ready():
    print(f"봇 로그인 완료: {bot.user}")

# Cog 자동 로드 (__init__.py 제외)
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def setup_hook():
    await load_cogs()

bot.run(TOKEN)
