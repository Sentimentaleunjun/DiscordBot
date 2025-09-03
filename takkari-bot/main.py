import os
import asyncio
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 읽기 허용 (필요 시)
bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        
   for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await bot.load_extension(f"cogs.{filename[:-3]}")
    
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
