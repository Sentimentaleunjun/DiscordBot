import os
import sys
import asyncio
import logging
from threading import Thread
import requests
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from flask import Flask, request

from takkari_bot.utils import db, logging_config

# ---------- Logging ----------
logger = logging_config.setup_logging()
logger.info("로그 시작")

# ---------- DB ----------
try:
    db.init_db()
    logger.info("✅ DB 초기화 완료")
except Exception as e:
    logger.exception("❌ DB 초기화 실패: %s", e)

# ---------- Flask ----------
app = Flask("takkari_bot")
PORT = int(os.environ.get("PORT", 10000))

@app.route("/")
def index():
    return "Takkari Bot - Healthy"

@app.route("/riot/callback")
def riot_callback():
    code = request.args.get("code")
    state = request.args.get("state")  # Discord user id
    if not code or not state:
        return "Missing code or state", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.environ.get("RIOT_REDIRECT_URI"),
        "client_id": os.environ.get("RIOT_CLIENT_ID"),
        "client_secret": os.environ.get("RIOT_CLIENT_SECRET")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://auth.riotgames.com/token", data=data, headers=headers)
    if r.status_code != 200:
        return f"Token request failed: {r.text}", 400

    token_data = r.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expiry = datetime.utcnow() + timedelta(seconds=token_data.get("expires_in",3600))

    # 유저 정보 가져오기
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get("https://riotgames.com/userinfo", headers=headers).json()
    summoner_name = user_info.get("name","Unknown")

    db.add_or_update_riot_user(state, summoner_name, access_token, refresh_token, expiry)
    return f"로그인 성공! {summoner_name}. 디스코드로 돌아가세요."

def run_flask():
    logger.info(f"Flask 서버 시작: {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

Thread(target=run_flask, daemon=True).start()

# ---------- Discord Bot ----------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# ---------- Auto Cog Load ----------
COGS = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.updown",
    "takkari_bot.cogs.riot"
]

for cog in COGS:
    try:
        bot.load_extension(cog)
        logger.info(f"✅ {cog} 로드 완료")
    except Exception as e:
        logger.exception(f"❌ {cog} 로드 실패: {e}")

# ---------- Presence ----------
PRESENCE_MESSAGES = [
    "🔥 {guild_count}개의 서버 관리",
    "🚀 업데이트 준비",
    "🤖 AI로 코딩"
]

@tasks.loop(seconds=20)
async def rotate_presence():
    guild_count = len(bot.guilds)
    for msg in PRESENCE_MESSAGES:
        name = msg.format(guild_count=guild_count)
        await bot.change_presence(activity=discord.Game(name=name))
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    logger.info(f"로그인 성공: {bot.user} ({bot.user.id})")
    if not rotate_presence.is_running():
        rotate_presence.start()

    try:
        synced = await bot.tree.sync()
        logger.info(f"🌐 슬래시 명령어 동기화 완료: {len(synced)}개")
    except Exception as e:
        logger.exception(f"❌ 슬래시 명령어 동기화 실패: {e}")

@bot.event
async def on_app_command_error(interaction, error):
    logger.exception(f"앱 커맨드 에러: {error}")
    try:
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ 명령어 처리 중 오류 발생", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ 명령어 처리 중 오류 발생", ephemeral=True)
    except:
        logger.exception("에러 피드백 전송 실패")

# ---------- Run ----------
def start_bot():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN 미설정, 종료")
        sys.exit(1)
    bot.run(token)

if __name__ == "__main__":
    start_bot()
