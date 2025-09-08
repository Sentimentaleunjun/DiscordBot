# main.py
import discord
from discord.ext import commands
import os
import logging
from flask import Flask
from threading import Thread

# -------------------- 로그 설정 --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Discord 봇 설정 --------------------
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 접근 필요
intents.members = True          # 멤버 관련 이벤트 필요

bot = commands.Bot(command_prefix="/", intents=intents)

# -------------------- Flask 서버 --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

# -------------------- Cog 자동 로딩 --------------------
async def load_cogs():
    extensions = [
        "takkari_bot.cogs.help",
        "takkari_bot.cogs.schedule",
        "takkari_bot.cogs.patchnote",
        "takkari_bot.cogs.support",
        "takkari_bot.cogs.userinfo",
        "takkari_bot.cogs.db_lookup",
        "takkari_bot.cogs.loglookup",
        "takkari_bot.cogs.dm_feature",
        "takkari_bot.cogs.accordingtobot",
        "takkari_bot.cogs.announce"
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Loaded extension: {ext}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {ext}: {e}")

# -------------------- 봇 이벤트 --------------------
@bot.event
async def on_ready():
    logger.info(f"✅ 로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="2.0 출시 준비🎉"))

@bot.event
async def setup_hook():
    # 기본 help 제거
    bot.remove_command("help")
    # Cog 로드
    await load_cogs()
    # 슬래시 명령어 동기화 (Global)
    synced = await bot.tree.sync()
    logger.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료 (Global)")

# -------------------- 봇 실행 --------------------
if __name__ == "__main__":
    # Flask 서버 별 Thread로 실행
    t = Thread(target=run_web)
    t.start()

    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        logger.error("❌ DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")
        exit(1)

    bot.run(TOKEN)
