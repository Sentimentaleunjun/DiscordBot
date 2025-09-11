import os
import sys
import asyncio
import logging
from threading import Thread

import discord
from discord.ext import commands, tasks
from flask import Flask

# 프로젝트 내부 유틸
from takkari_bot.utils import db, logging_config

# ---------- 로깅 설정 ----------
logger = logging_config.setup_logging()  # shared/bot.log 와 콘솔에 로깅
logger.info("로그 시작")

# ---------- DB 초기화 ----------
try:
    db.init_db()
    logger.info("✅ DB 초기화 완료")
except Exception as e:
    logger.exception("❌ DB 초기화 실패: %s", e)

# ---------- Flask (웹 헬스체크 / OAuth callback 등 용도) ----------
app = Flask("takkari_bot")

@app.route("/")
def index():
    return "Takkari Bot - web endpoint (healthy)"

# Render는 PORT 환경변수 사용
PORT = int(os.environ.get("PORT", 10000))

def run_flask():
    logger.info("Flask 서버 시작 (포트 %s)", PORT)
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# 별도 스레드에서 실행
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

# ---------- Discord Bot 설정 (discord.py 사용) ----------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# ---------- COG 목록 ----------
COGS = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.help"
]

# ---------- Presence(상태) 순환 ----------
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

# ---------- Cog 로드 ----------
async def load_cogs():
    loaded = 0
    for cog in COGS:
        try:
            await bot.load_extension(cog)  # ✅ 비동기 로드
            logger.info("✅ %s 로드 완료", cog)
            print(f"✅ {cog} 로드 완료")
            loaded += 1
        except Exception as e:
            logger.exception("❌ %s 로드 실패: %s", cog, e)
            print(f"❌ {cog} 로드 실패: {e}")
    logger.info("총 시도한 코그: %d, 성공: %d", len(COGS), loaded)

# ---------- 이벤트 ----------
@bot.event
async def on_ready():
    logger.info("로그인 성공: %s (ID: %s)", bot.user, bot.user.id)
    print(f"로그인 성공: {bot.user} (ID: {bot.user.id})")

    # 코그 로드
    await load_cogs()

    # 슬래시 커맨드 동기화 (글로벌)
    try:
        synced = await bot.tree.sync()
        logger.info("🌐 슬래시 명령어 동기화 완료: %d개", len(synced))
        print(f"🌐 슬래시 명령어 동기화 완료: {len(synced)}개")
    except Exception as e:
        logger.exception("❌ 슬래시 명령어 동기화 실패: %s", e)
        print(f"❌ 슬래시 명령어 동기화 실패: {e}")

    # 서버 수 출력
    try:
        guild_count = len(bot.guilds)
        logger.info("현재 접속 서버 수: %d", guild_count)
        print(f"현재 접속 서버 수: {guild_count}")
    except Exception:
        logger.exception("서버 수 확인 중 오류")

    # Presence 시작
    if not rotate_presence.is_running():
        rotate_presence.start()
        logger.info("Presence 순환 스타트")

# ---------- 예외 핸들링 ----------
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

# ---------- 시작 ----------
def start_bot():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("환경변수 DISCORD_BOT_TOKEN 이 설정되어 있지 않습니다.")
        print("환경변수 DISCORD_BOT_TOKEN 이 설정되어 있지 않습니다.")
        sys.exit(1)

    logger.info("봇 시작 시도")
    bot.run(token)

if __name__ == "__main__":
    start_bot()