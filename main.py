import os
import asyncio
import discord
from discord.ext import commands
from utils.db import init_db

from support-web.app import app  # 웹서비스 가져오기
import threading
import uvicorn

# 환경변수
TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("DEV_ID", "0"))

# Discord Intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# DB 초기화
init_db()

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")

async def start_bot():
    # cogs 로드
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
    # 웹서버를 별도 스레드로 실행
    threading.Thread(target=start_web, daemon=True).start()

    # 비동기 루프에서 디스코드 봇 실행
    asyncio.run(start_bot())
