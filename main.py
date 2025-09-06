# main.py
import os
import logging
import discord
from discord.ext import commands, tasks
from threading import Thread
from flask import Flask

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 5000))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Flask 서버 ----
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ 따까리봇 실행 중입니다!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

# ---- Presence(상태) ----
status_messages = [
    "GSEJ Company 공식 봇",
    "당신의 디스코드 도우미",
    "Server.. Update"
]
index = 0

@tasks.loop(seconds=30)  # 30초마다 상태 변경
async def cycle_status():
    global index
    await bot.change_presence(
        activity=discord.Game(name=status_messages[index])
    )
    index = (index + 1) % len(status_messages)

# ---- 이벤트 ----
@bot.event
async def on_ready():
    logging.info("🤖 Logged in as %s (%s)", bot.user, bot.user.id)
    if not cycle_status.is_running():
        cycle_status.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Thread(target=run_web).start()
    bot.run(TOKEN)
