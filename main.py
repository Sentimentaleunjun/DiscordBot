import os
import sys
import asyncio
import logging
from threading import Thread

import discord
from discord.ext import commands, tasks
from flask import Flask, request, redirect, session, jsonify

import requests
from db import init_db

# ---------- 로깅 ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("takkari_bot")

# ---------- DB ----------
init_db()

# ---------- Flask ----------
app = Flask("takkari_bot")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

RIOT_CLIENT_ID = os.environ.get("RIOT_CLIENT_ID")
RIOT_CLIENT_SECRET = os.environ.get("RIOT_CLIENT_SECRET")
RIOT_REDIRECT_URI = os.environ.get("RIOT_REDIRECT_URI")

# 세션 기반 간단한 로그인 상태 (예시)
user_tokens = {}

@app.route("/")
def index():
    return "Takkari Bot - web endpoint (healthy)"

@app.route("/riot/login/<discord_id>")
def riot_login(discord_id):
    # 사용자를 Riot OAuth2 로그인으로 리다이렉트
    url = (
        f"https://auth.riotgames.com/authorize"
        f"?client_id={RIOT_CLIENT_ID}"
        f"&redirect_uri={RIOT_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid"
        f"&state={discord_id}"
    )
    return redirect(url)

@app.route("/riot/callback")
def riot_callback():
    code = request.args.get("code")
    state = request.args.get("state")  # discord_id
    if not code or not state:
        return "⚠️ OAuth2 코드나 상태 없음", 400

    # 코드 -> 액세스 토큰
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": RIOT_REDIRECT_URI,
        "client_id": RIOT_CLIENT_ID,
        "client_secret": RIOT_CLIENT_SECRET
    }
    resp = requests.post("https://auth.riotgames.com/token", data=data)
    if resp.status_code != 200:
        return f"토큰 교환 실패: {resp.text}", 400

    token_info = resp.json()
    user_tokens[state] = token_info  # discord_id 기준 저장
    return f"로그인 완료! Discord로 돌아가세요."

# ---------- Flask 스레드 ----------
PORT = int(os.environ.get("PORT", 10000))
def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)
Thread(target=run_flask, daemon=True).start()

# ---------- Discord Bot ----------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# ---------- Cog 로드 ----------
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
for cog in COGS:
    try:
        bot.load_extension(cog)
    except Exception as e:
        logger.exception("%s 로드 실패: %s", cog, e)

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
    print(f"로그인 성공: {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()
    if not rotate_presence.is_running():
        rotate_presence.start()

@bot.event
async def on_app_command_error(interaction, error):
    await interaction.response.send_message("⚠️ 명령어 처리 중 오류 발생", ephemeral=True)

# ---------- Riot 전적 조회 명령어 ----------
@bot.tree.command(name="riot_login", description="Riot 계정 로그인")
async def riot_login_cmd(interaction: discord.Interaction):
    url = f"https://ddaggaribos-0-8beta.onrender.com/riot/login/{interaction.user.id}"
    await interaction.response.send_message(f"로그인하려면 클릭: {url}", ephemeral=True)

@bot.tree.command(name="riot_stats", description="자기 Riot 전적 조회")
async def riot_stats_cmd(interaction: discord.Interaction):
    token_info = user_tokens.get(str(interaction.user.id))
    if not token_info:
        await interaction.response.send_message("⚠️ 먼저 /riot_login 으로 로그인하세요", ephemeral=True)
        return

    access_token = token_info.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.riotgames.com/lol/summoner/v4/summoners/me", headers=headers)
    if resp.status_code != 200:
        await interaction.response.send_message(f"전적 조회 실패: {resp.text}", ephemeral=True)
        return

    data = resp.json()
    await interaction.response.send_message(f"소환사 정보: {data}", ephemeral=True)

# ---------- 시작 ----------
def start_bot():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        sys.exit("DISCORD_BOT_TOKEN 미설정")
    bot.run(token)

if __name__ == "__main__":
    start_bot()
