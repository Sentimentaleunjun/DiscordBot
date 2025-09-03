import os
import discord
from discord.ext import commands
from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = 909360134566862878  # Restart는 개발자만 가능

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()  # DB 초기화

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ 봇 로그인 완료: {bot.user}")

# cogs 자동 로드
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
