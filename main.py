# main.py
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
    # debug=False (프로덕션용) — 개발용이면 True로 바꿔도 됨
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# 별도 스레드에서 실행
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

# ---------- Discord Bot 설정 (discord.py 사용) ----------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # 멤버 관련 정보가 필요하면 True

# commands.Bot 사용 (슬래시 명령어는 bot.tree로 관리)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------- COG 목록 (파일명 기준, fun 제외) ----------
COGS = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.addschedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.help"
]

# ---------- Cog 로드 (동기 로드) ----------
loaded = 0
for cog in COGS:
    try:
        bot.load_extension(cog)
        logger.info("✅ %s 로드 완료", cog)
        print(f"✅ {cog} 로드 완료")
        loaded += 1
    except Exception as e:
        logger.exception("❌ %s 로드 실패: %s", cog, e)
        print(f"❌ {cog} 로드 실패: {e}")

logger.info("총 시도한 코그: %d, 성공: %d", len(COGS), loaded)

# ---------- Presence(상태) 순환 (서버 수 반영) ----------
# 원문 요청에 맞춰 문자열(앞에 이모지)로 표시 — '하는중' 같은 서술은 피함
PRESENCE_MESSAGES = [
    "🔥 {guild_count}개의 서버 관리중",
    "🚀 업데이트 준비",
    "🤖 AI로 코딩"
]

@tasks.loop(seconds=20)
async def rotate_presence():
    try:
        guild_count = len(bot.guilds)
        for msg in PRESENCE_MESSAGES:
            # format guild_count into string
            name = msg.format(guild_count=guild_count)
            await bot.change_presence(activity=discord.Game(name=name))
            logger.debug("Presence 변경: %s", name)
            # sleep between each presence step (but tasks.loop will sleep between iterations)
            await asyncio.sleep(10)
    except Exception:
        logger.exception("Presence 순환 중 오류 발생")

@bot.event
async def on_ready():
    # This event can fire multiple times when reconnecting; guard prints accordingly.
    logger.info("로그인 성공: %s (ID: %s)", bot.user, bot.user.id)
    print(f"로그인 성공: {bot.user} (ID: {bot.user.id})")

    # 슬래시 커맨드 동기화 (글로벌)
    try:
        synced = await bot.tree.sync()  # 글로벌 동기화
        # discord.py returns a list of commands that were synced
        logger.info("🌐 슬래시 명령어 동기화 완료: %d개", len(synced))
        print(f"🌐 슬래시 명령어 동기화 완료: {len(synced)}개")
    except Exception as e:
        logger.exception("❌ 슬래시 명령어 동기화 실패: %s", e)
        print(f"❌ 슬래시 명령어 동기화 실패: {e}")

    # 서버수 출력
    try:
        guild_count = len(bot.guilds)
        logger.info("현재 접속 서버 수: %d", guild_count)
        print(f"현재 접속 서버 수: {guild_count}")
    except Exception:
        logger.exception("서버 수 확인 중 오류")

    # Presence 시작 (이미 실행중이면 건너뜀)
    if not rotate_presence.is_running():
        rotate_presence.start()
        logger.info("Presence 순환 스타트")
    else:
        logger.info("Presence 순환 이미 실행 중")

# ---------- 예외 핸들링 (인터랙션 관련 알 수 없는 interaction 에러 방지용) ----------
@bot.event
async def on_app_command_error(interaction, error):
    # discord.app_commands.errors.CommandInvokeError 등 다양한 에러가 여기에 들어올 수 있음
    logger.exception("앱 커맨드 실행 중 예외: %s", error)
    # 가능한 경우 사용자에게 간단한 피드백
    try:
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ 명령어 처리 중 오류가 발생했습니다.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ 명령어 처리 중 오류가 발생했습니다.", ephemeral=True)
    except Exception:
        logger.exception("에러 피드백 전송 중 예외")

# ---------- 시작 (토큰 검사 후 실행) ----------
def start_bot():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("환경변수 DISCORD_BOT_TOKEN 이 설정되어 있지 않습니다. 프로세스를 종료합니다.")
        print("환경변수 DISCORD_BOT_TOKEN 이 설정되어 있지 않습니다. 프로세스를 종료합니다.")
        sys.exit(1)

    # 실행 (blocking)
    logger.info("봇 시작 시도")
    bot.run(token)

if __name__ == "__main__":
    start_bot()
