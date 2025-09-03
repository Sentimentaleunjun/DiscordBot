import os
import discord
from discord.ext import commands
from utils.db import init_db

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = 909360134566862878  # restart 전용 권한

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

init_db()
bot.run(TOKEN)
