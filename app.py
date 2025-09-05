import os
import threading
from flask import Flask, render_template
import discord
from discord.ext import commands
from takkari-bot.utils.db import init_db

# ------------------------
# Flask Web
# ------------------------
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ------------------------
# Discord Bot
# ------------------------
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")

async def load_cogs():
    for filename in os.listdir("./takkari-bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"takkari-bot.cogs.{filename[:-3]}")

async def start_bot():
    await load_cogs()
    await bot.start(TOKEN)

def run_bot():
    import asyncio
    asyncio.run(start_bot())

# ------------------------
# 실행
# ------------------------
if __name__ == "__main__":
    # DB 초기화
    init_db()

    # 디스코드 봇 스레드 실행
    t = threading.Thread(target=run_bot)
    t.start()

    # Flask 실행 (Render에서 포트 필요)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)