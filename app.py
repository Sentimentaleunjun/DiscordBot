import os
import threading
import asyncio
from flask import Flask, render_template
import discord
from discord.ext import commands
from takkari_bot.utils.db import init_db   # utils/db.py 에 있는 init_db 불러오기

# ------------------------
# Flask Web
# ------------------------
app = Flask(__name__, template_folder="support-web/templates")

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
if not TOKEN:
    raise ValueError("❌ 환경변수 DISCORD_TOKEN 이 설정되지 않았습니다!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")

async def load_cogs():
    """cogs 폴더 안의 모든 확장 불러오기"""
    for filename in os.listdir("./takkari-bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"takkari_bot.cogs.{filename[:-3]}")

async def start_bot():
    await load_cogs()
    await bot.start(TOKEN)

def run_bot():
    asyncio.run(start_bot())

# ------------------------
# 실행
# ------------------------
if __name__ == "__main__":
    # DB 초기화 (shared/user.db 등)
    init_db()

    # 디스코드 봇은 스레드로 실행
    t = threading.Thread(target=run_bot)
    t.start()

    # Flask 실행 (Render는 반드시 0.0.0.0 + PORT 사용)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)