import os
import discord
from discord.ext import commands
from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = 909360134566862878

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()

# 변경 후
intents = discord.Intents.all()

class TakkariBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()

bot = TakkariBot()

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user}")

bot.run(TOKEN)

