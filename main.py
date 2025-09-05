import os
import asyncio
import discord
from discord.ext import commands
from utils.db import init_db

from support_web.app import app 
import threading
import uvicorn

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("DEV_ID", "0"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")

async def start_bot():
    
    for filename in os.listdir("./takkari-bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📂 Cog 로드 완료: {filename}")
            except Exception as e:
                print(f"❌ Cog 로드 실패: {filename} -> {e}")

    if not TOKEN:
        raise ValueError("❌ DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")
    await bot.start(TOKEN)

def start_web():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=start_web, daemon=True).start()
    asyncio.run(start_bot())
