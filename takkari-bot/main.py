import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
bot.admin_id = ADMIN_ID

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user}")

async def load_cogs():
    for filename in os.listdir("./takkari-bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"takkari-bot.cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
