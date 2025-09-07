import discord
from discord.ext import commands
import logging
from flask import Flask
from threading import Thread
import os
from takkari_bot.utils.db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- Flask 서버 ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# ---------- Cog 로딩 ----------
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
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"✅ Loaded extension: {ext}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {ext}: {e}")

@bot.event
async def on_ready():
    logger.info(f"✅ 로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="따까리봇 2.0 준비"))

@bot.event
async def setup_hook():
    bot.remove_command("help")
    init_db()        # DB 초기화
    await load_cogs()
    synced = await bot.tree.sync()
    logger.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료 (Global)")

if __name__ == "__main__":
    Thread(target=run_web).start()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
