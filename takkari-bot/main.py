import os
import discord
from discord.ext import commands
from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = 909360134566862878

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()

@bot.event
async def on_ready():
    print(f"봇 로그인 완료: {bot.user}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
