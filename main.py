import os
import sys
import asyncio
import logging
from threading import Thread

import discord
from discord.ext import commands, tasks
from flask import Flask, request, jsonify

# 프로젝트 내부 유틸
from takkari_bot.utils import db, logging_config

# ---------- 로깅 설정 ----------
logger = logging_config.setup_logging()
logger.info("로그 시작")

# ---------- DB 초기화 ----------
try:
    db.init_db()
    logger.info("✅ DB 초기화 완료")
except Exception as e:
    logger.exception("❌ DB 초기화 실패: %s", e)

# ---------- Flask 서버 ----------
app = Flask("takkari_bot")

@app.route("/")
def index():
    return "Main Server is Running! (beta version GSEJ)"

# ---------- Riot Callback ----------
@app.route("/riot/callback", methods=["POST"])
def riot_callback():
    data = request.json
    logger.info("Riot Callback 수신: %s", data)
    return jsonify({"status": "ok"}), 200

PORT = int(os.environ.get("PORT", 10000))

def run_flask():
    logger.info("Flask 서버 시작 (포트 %s)", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# ---------- Discord Bot 설정 ----------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# ---------- Discord 로그 핸들러 ----------
class DiscordLogHandler(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.loop.create_task(self.send_log(log_entry))

    async def send_log(self, log_entry):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            if len(log_entry) > 1900:
                log_entry = log_entry[:1900] + "..."
            await channel.send(f"```{log_entry}```")

LOG_CHANNEL_ID = 1417052732019310652
discord_handler = DiscordLogHandler(bot, LOG_CHANNEL_ID)
discord_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s | %(message)s')
discord_handler.setFormatter(formatter)
logger.addHandler(discord_handler)

# ---------- COG 목록 ----------
COGS = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.announce",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.dblookup",
    "takkari_bot.cogs.riot",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.help"
]

# ---------- Cog 로드 ----------
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

# ---------- Presence 순환 ----------
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
            await asyncio.sleep(10)
    except Exception:
        logger.exception("Presence 순환 중 오류 발생")

# ---------- 이벤트 ----------
@bot.event
async def on_ready():
    logger.info("로그인 성공: %s (ID: %s)", bot.user, bot.user.id)
    logger.info("현재 접속 서버 수: %d", len(bot.guilds))

    if not rotate_presence.is_running():
        rotate_presence.start()

    # 글로벌 슬래시 명령어 동기화
    try:
        synced = await bot.tree.sync()
        logger.info("🌐 글로벌 동기화 완료: %d개", len(synced))
    except Exception as e:
        logger.exception("❌ 슬래시 명령어 동기화 실패: %s", e)

# ---------- 앱 커맨드 에러 ----------
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

# ---------- 봇 & Flask 동시 실행 ----------
async def main():
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("환경변수 DISCORD_BOT_TOKEN 미설정")
        sys.exit(1)

    await load_cogs()
    logger.info("봇 시작 시도")
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("종료됨")