import os
import logging
from flask import Flask
from threading import Thread

import discord
from discord.ext import commands

from takkari_bot.utils import logging_config
from takkari_bot.utils.db import init_support_table, init_points_table, init_quiz_table

# -------------------- Flask --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "이 웹사이트는 따까리봇 실행 백팅업 사이트입니다"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

# -------------------- Discord --------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.fun",
]

@bot.event
async def on_ready():
    logging.info(f"✅ {bot.user} is connected and running!")
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ {len(synced)} 개의 슬래시 명령어 동기화 완료 (Global)")
    except Exception as e:
        logging.error(f"❌ 슬래시 명령어 동기화 실패: {e}")

def main():
    # DB 초기화
    init_support_table()
    init_points_table()
    init_quiz_table()

    # Flask 실행
    Thread(target=run_flask).start()

    # Discord 실행
    for cog in COGS:
        try:
            bot.load_extension(cog)
            logging.info(f"✅ Loaded extension: {cog}")
        except Exception as e:
            logging.error(f"❌ Failed to load extension {cog}: {e}")

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    bot.run(token)

if __name__ == "__main__":
    main()
