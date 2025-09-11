import os
import asyncio
import discord
from discord.ext import tasks
from flask import Flask
from takkari_bot.utils import db

# ---------------- Flask 서버 ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# ---------------- Discord Bot ----------------
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 읽기 권한
bot = discord.Bot(intents=intents)  # 슬래시 전용

# Presence 상태 리스트
statuses = [
    lambda: f"🔥 {len(bot.guilds)}개의 서버 관리",
    lambda: "🚀 업데이트 준비",
    lambda: "🤖 AI로 코딩"
]

# Presence 변경 task
@tasks.loop(seconds=15)
async def change_presence():
    status = discord.Game(next(change_presence.status_cycle))
    await bot.change_presence(activity=status)

# Presence 순환 iterator
import itertools
change_presence.status_cycle = itertools.cycle(statuses)

# ---------------- Bot 이벤트 ----------------
@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user} (ID: {bot.user.id})")
    
    # DB 초기화
    db.init_db()
    
    # 슬래시 명령어 글로벌 동기화
    try:
        await bot.tree.sync()
        print("✅ Global slash commands synchronized")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")
    
    # Presence 시작
    change_presence.start()

# ---------------- Cog 로드 ----------------
cogs = [
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

async def load_cogs():
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ {cog} loaded")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

# ---------------- Run ----------------
async def main():
    # Cog 로드
    await load_cogs()

    # Bot 실행
    await bot.start(os.environ["DISCORD_BOT_TOKEN"])

# Flask 서버와 Bot 동시 실행
def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    start_flask()