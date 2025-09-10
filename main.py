# main.py
import discord
from discord.ext import commands, tasks
from discord import app_commands
from flask import Flask
import os
import asyncio

# --------- Flask 웹서비스 (Render용) ---------
app = Flask(__name__)

@app.route("/")
def home():
    return "따까리봇 1.0 정식출시! 🎉"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# --------- Discord Bot 설정 ---------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 순환할 Presence 메시지
status_messages = [
    "{guild_count}개의 서버 관리중🔥",
    "업데이트 준비중🚀",
    "🤖AI로 코딩중"
]

@tasks.loop(seconds=30)
async def update_presence():
    guild_count = len(bot.guilds)
    message = status_messages[update_presence.current_index].format(guild_count=guild_count)
    activity = discord.Activity(type=discord.ActivityType.watching, name=message)
    await bot.change_presence(activity=activity)
    update_presence.current_index = (update_presence.current_index + 1) % len(status_messages)

update_presence.current_index = 0

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료!")
    await bot.tree.sync()
    update_presence.start()

# --------- Cogs 불러오기 ---------
extensions = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.fun",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.accordingtobot"
]

async def load_extensions():
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ {ext} 로드 완료")
        except Exception as e:
            print(f"❌ {ext} 로드 실패: {e}")

# --------- 메인 실행 ---------
async def main():
    await load_extensions()
    # Flask 웹서버와 Discord 봇 동시에 실행
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.to_thread(run_web))
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())