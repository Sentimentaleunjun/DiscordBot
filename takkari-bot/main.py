import os
import threading
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
import aiohttp
import sqlite3
import logging

# 로깅 설정 (모든 로그를 bot.log에 기록)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# DB 연결 (키 저장)
conn = sqlite3.connect("bot.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS keys (service TEXT PRIMARY KEY, api_key TEXT)")
conn.commit()

async def get_api_key(service: str):
    env_key = os.getenv(service.upper() + "_KEY")
    if env_key:
        return env_key
    cur.execute("SELECT api_key FROM keys WHERE service = ?", (service,))
    row = cur.fetchone()
    return row[0] if row else None

@bot.event
async def on_ready():
    await tree.sync()
    logging.info(f"봇 로그인 완료: {bot.user}")
    print(f"봇 로그인 완료: {bot.user}")

@bot.event
async def on_command(ctx):
    logging.info(f"{ctx.author} 사용자가 명령어 실행: {ctx.command}")

@tree.command(name="ping", description="봇의 핑 확인")
async def ping(interaction: discord.Interaction):
    logging.info(f"{interaction.user} -> /ping 실행")
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@tree.command(name="restart", description="봇 재시작 (개발자만 가능)")
async def restart(interaction: discord.Interaction):
    logging.info(f"{interaction.user} -> /restart 실행 시도")
    if interaction.user.id != 909360134566862878:
        await interaction.response.send_message("이 명령어는 개발자만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message("봇을 재시작합니다...", ephemeral=True)
    logging.warning("봇이 수동 재시작됩니다.")
    os._exit(1)

@tree.command(name="serverinfo", description="서버 정보를 표시합니다.")
async def serverinfo(interaction: discord.Interaction):
    logging.info(f"{interaction.user} -> /serverinfo 실행")
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, description="서버 정보", color=discord.Color.blue())
    embed.add_field(name="멤버 수", value=guild.member_count)
    embed.add_field(name="서버 ID", value=guild.id)
    embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo", description="유저 정보를 표시합니다.")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    logging.info(f"{interaction.user} -> /userinfo 실행 (대상: {user or interaction.user})")
    user = user or interaction.user
    embed = discord.Embed(title=f"{user}", color=discord.Color.green())
    embed.add_field(name="유저 ID", value=user.id)
    embed.add_field(name="계정 생성일", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="서버 참가일", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    await interaction.response.send_message(embed=embed)

@tree.command(name="weather", description="날씨를 확인합니다.")
async def weather(interaction: discord.Interaction, city: str):
    logging.info(f"{interaction.user} -> /weather {city} 실행")
    key = await get_api_key("weather")
    if not key:
        await interaction.response.send_message("WeatherAPI 키가 설정되지 않았습니다.", ephemeral=True)
        return
    async with aiohttp.ClientSession() as session:
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}"
        async with session.get(url) as resp:
            if resp.status != 200:
                logging.error(f"/weather {city} 요청 실패: {resp.status}")
                await interaction.response.send_message("날씨 정보를 가져올 수 없습니다.", ephemeral=True)
                return
            data = await resp.json()
            embed = discord.Embed(title=f"{city}의 날씨", color=discord.Color.orange())
            embed.add_field(name="상태", value=data['current']['condition']['text'])
            embed.add_field(name="온도", value=f"{data['current']['temp_c']}°C")
            embed.set_thumbnail(url="https:" + data['current']['condition']['icon'])
            await interaction.response.send_message(embed=embed)

@tree.command(name="ask", description="GPT에게 질문합니다.")
async def ask(interaction: discord.Interaction, *, question: str):
    logging.info(f"{interaction.user} -> /ask 실행: {question}")
    key = await get_api_key("openai")
    if not key:
        await interaction.response.send_message("OpenAI API 키가 설정되지 않았습니다.", ephemeral=True)
        return
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        json = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 200
        }
        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json) as resp:
            if resp.status != 200:
                logging.error(f"/ask GPT 요청 실패: {resp.status}")
                await interaction.followup.send("GPT 요청 실패")
                return
            data = await resp.json()
            answer = data["choices"][0]["message"]["content"]
            await interaction.followup.send(answer)

# Flask 서버 (Render 무료 유지용)
app = Flask(__name__)
@app.route("/")
def home():
    return "봇이 정상 작동 중입니다! 2025 GSEJ Company in Render"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

bot.run(os.getenv("DISCORD_TOKEN"))