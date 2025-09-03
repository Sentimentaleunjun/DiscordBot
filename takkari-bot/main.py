import os
import discord
from discord.ext import commands
from fastapi import FastAPI, Request
import uvicorn
import asyncio
from utils.db import init_db, get_support_tickets

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== FastAPI 서버 =====
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "봇은 정상적으로 실행 중입니다."}

@app.get("/support")
async def view_support(request: Request):
    key = request.query_params.get("key")
    admin_key = os.getenv("ADMIN_KEY")

    if key != admin_key:
        return {"error": "인증 실패. 관리자만 접근 가능합니다."}

    tickets = get_support_tickets()
    return {"tickets": tickets}

# ===== Discord Bot + FastAPI 같이 실행 =====
async def start_bot():
    async with bot:
        await bot.start(TOKEN)

def run():
    loop = asyncio.get_event_loop()

    # FastAPI 실행 (서브 스레드)
    config = uvicorn.Config(app, host="0.0.0.0", port=10000, log_level="info")
    server = uvicorn.Server(config)

    loop.create_task(server.serve())
    loop.run_until_complete(start_bot())

if __name__ == "__main__":
    init_db()
    run()