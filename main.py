import os
import sys
import asyncio
import logging
from threading import Thread

import discord
from discord.ext import commands, tasks
from flask import Flask
from takkari_bot.utils import db, logging_config

logger = logging_config.setup_logging()
logger.info("로그 시작")

try:
    db.init_db()
    logger.info("✅ DB 초기화 완료")
except Exception as e:
    logger.exception("❌ DB 초기화 실패: %s", e)

app = Flask("takkari_bot")

@app.route("/")
def index():
    return "Takkari Bot - healthy"

PORT = int(os.environ.get("PORT", 10000))

def run_flask():
    logger.info("Flask 서버 시작 (포트 %s)", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)


COGS = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.riot",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.updown",
    "takkari_bot.cogs.help"
]

async def load_cogs():
    loaded = 0
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logger.info("✅ %s 로드 완료", cog)
            loaded += 1
        except Exception as e:
            logger.exception("❌ %s 로드 실패: %s", cog, e)
    logger.info("총 시도한 코그: %d, 성공: %d", len(COGS), loaded)

PRESENCE_MESSAGES = [
    "🔥 {guild_count}개의 서버 관리",
    "🚀 업데이트 준비",
    "🤖 AI로 코딩"
]

@tasks.loop(seconds=20)
async def rotate_presence():
    try:
        guild_count = len(bot.guilds)
        for msg in PRESENCE_MESSAGES:
            name = msg.format(guild_count=guild_count)
            await bot.change_presence(activity=discord.Game(name=name))
            logger.debug("Presence 변경: %s", name)
            await asyncio.sleep(10)
    except Exception:
        logger.exception("Presence 순환 중 오류 발생")

@bot.event
async def on_ready():
    logger.info("로그인 성공: %s (ID: %s)", bot.user, bot.user.id)
    print(f"로그인 성공: {bot.user} (ID: {bot.user.id})")

    await load_cogs()

    try:
        synced = await bot.tree.sync()
        logger.info("🌐 슬래시 명령어 동기화 완료: %d개", len(synced))
        print(f"🌐 슬래시 명령어 동기화 완료: {len(synced)}개")
    except Exception as e:
        logger.exception("❌ 슬래시 명령어 동기화 실패: %s", e)


    if not rotate_presence.is_running():
        rotate_presence.start()
        logger.info("Presence 순환 스타트")

@bot.event
async def on_app_command_error(interaction, error):
    logger.exception("앱 커맨드 실행 중 예외: %s", error)
    try:
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ 명령어 처리 중 오류가 발생했습니다.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ 명령어 처리 중 오류가 발생했습니다.", ephemeral=True)
    except Exception:
        logger.exception("에러 피드백 전송 중 예외")


def start_bot():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("환경변수 DISCORD_BOT_TOKEN 미설정")
        sys.exit(1)
    bot.run(token)

if __name__ == "__main__":
    start_bot()
