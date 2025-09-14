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
    "takkari_bot.cogs.dm_feature",  # DM 전송 관련 코그
    "takkari_bot.cogs.help"
]

# ---------- Cog 로드 ----------
async def load_cogs():
    loaded = 0
    for cog in COGS:
        try:
            await bot.load_extension(cog)  # ✅ await 추가
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

# ---------- 서버 입장 시 개발자용 안내 DM ----------
@bot.event
async def on_guild_join(guild: discord.Guild):
    owner = guild.owner
    if owner is None:
        return
    try:
        dm_channel = owner.dm_channel
        if dm_channel is None:
            dm_channel = await owner.create_dm()

        from discord.ui import View, Button
        view = View()
        guide_button = Button(
            label="🔥사용가이드", 
            url="https://gsej-company.onrender.com/takkari-bot.html"
        )
        view.add_item(guide_button)

        embed = discord.Embed(
            title="👋 따까리봇 개발자용 안내",
            description="안녕하세요! 서버에 봇을 추가해주셔서 감사합니다!\n아래 버튼을 눌러 개발자용 사용가이드를 확인하세요.",
            color=discord.Color.blue()
        )

        await dm_channel.send(embed=embed, view=view)
        logger.info(f"✅ {guild.name} 서버 소유자에게 개발자용 안내 DM 전송 완료")
    except Exception as e:
        logger.exception(f"❌ {guild.name} 서버 소유자 DM 전송 실패: {e}")

# ---------- 이벤트 ----------
@bot.event
async def on_ready():
    logger.info("로그인 성공: %s (ID: %s)", bot.user, bot.user.id)

    try:
        logger.info("🌐 슬래시 명령어 동기화 완료: %d개", len(bot.tree.get_commands()))
    except Exception as e:
        logger.exception("❌ 슬래시 명령어 동기화 실패: %s", e)

    logger.info("현재 접속 서버 수: %d", len(bot.guilds))

    if not rotate_presence.is_running():
        rotate_presence.start()

@bot.event
async def setup_hook():
    await load_cogs()
    synced = await bot.tree.sync()  # 글로벌 동기화
    logger.info("🌐 글로벌 동기화 완료: %d개", len(synced))

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
    # Flask 먼저 스레드로 실행
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Discord Bot 실행
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("환경변수 DISCORD_BOT_TOKEN 미설정")
        sys.exit(1)

    logger.info("봇 시작 시도")
    await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("종료됨")
