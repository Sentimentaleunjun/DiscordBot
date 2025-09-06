import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def setup_hook():
    # Cogs 자동 로드
    for filename in os.listdir("takkari_bot/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"takkari_bot.cogs.{filename[:-3]}")
    # 🔥 슬래시 커맨드 등록
    await bot.tree.sync()
    print("✅ 슬래시 커맨드 등록 완료")

def run_discord_bot():
    bot.run(TOKEN)
