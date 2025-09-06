import discord
from discord.ext import commands
import os
import logging
from flask import Flask
from threading import Thread

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Discord 봇 intents
intents = discord.Intents.default()
intents.message_content = True  # DM 및 채팅 명령어 필요
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Flask 서버 (Render ping 유지용)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


# 이벤트: 봇 준비 완료
@bot.event
async def on_ready():
    logger.info(f"✅ 로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Game(name="2.0 출시 준비🎉")
    )

async def load_cogs():
    extensions = [
        "takkari_bot.cogs.help",       # help.py
        "takkari_bot.cogs.schedule",
        "takkari_bot.cogs.patchNote",
        "takkari_bot.cogs.support",
        "takkari_bot.cogs.userinfo",
        "takkari_bot.cogs.db_lookup",
        "takkari_bot.cogs.loglookup",
        "takkari_bot.cogs.dm_feature",
        "takkari_bot.cogs.accordingtobot",
    ]

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Loaded extension: {ext}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {ext}: {e}")

@bot.event
async def setup_hook():
    # 기본 help 명령어 제거 (충돌 방지)
    bot.remove_command("help")

    await load_cogs()

    synced = await bot.tree.sync()
    logger.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료 (Global)")

if __name__ == "__main__":
    # Render에서 Flask 웹 서버 실행
    t = Thread(target=run_web)
    t.start()

    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
