import os
import asyncio
import discord
from discord.ext import commands
from utils.db import init_db

# Dummy web server
from fastapi import FastAPI
import uvicorn
import threading

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()

# ---- Discord Bot ----
async def main_bot():
    async with bot:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await bot.load_extension(f"cogs.{filename[:-3]}")
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    print(f"봇 로그인 완료: {bot.user}")

# ---- Dummy Web Server ----
app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "Takkari Bot is running"}

def run_web():
    port = int(os.getenv("PORT", 5000))  # Render 제공 포트
    uvicorn.run(app, host="0.0.0.0", port=port)

# ---- Run Both ----
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    asyncio.run(main_bot())