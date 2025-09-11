import os
import random
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from takkari_bot.utils import logging_config, db

# ---------------- 로깅 ----------------
logger = logging_config.setup_logging()

# ---------------- Flask ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Takkari Bot is running!"

# ---------------- Discord ----------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- Presence ----------------
@tasks.loop(minutes=5)
async def update_presence():
    await bot.wait_until_ready()
    guild_count = len(bot.guilds)

    activities = [
        f"🔥 {guild_count}개의 서버 관리",
        "🚀 업데이트 준비",
        "🤖 AI로 코딩"
    ]
    activity = discord.Game(random.choice(activities))
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logger.info(f"Presence 업데이트됨: {activity.name}")

# ---------------- 이벤트 ----------------
@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        logger.info(f"슬래시 커맨드 동기화됨: {len(synced)}개")
    except Exception as e:
        logger.error(f"슬래시 커맨드 동기화 실패: {e}")
    update_presence.start()

# ---------------- Cog 로드 ----------------
initial_extensions = [
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

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        logger.info(f"✅ {ext.split('.')[-1]}.py 로드 성공")
    except Exception as e:
        logger.error(f"❌ {ext.split('.')[-1]}.py 로드 실패: {e}")

# ---------------- 실행 ----------------
if __name__ == "__main__":
    # DB 초기화
    db.init_db()

    # Render용 Flask
    import threading
    def run_flask():
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask).start()

    # Token 확인 + 실행
    token = os.getenv("DISCORD_BOT_TOKEN")

    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN 환경변수를 불러오지 못했습니다!")
    else:
        logger.info(f"✅ 토큰이 정상적으로 불러와졌습니다. 길이: {len(token)}")
        bot.run(token)