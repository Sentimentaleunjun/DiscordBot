import os
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import sqlite3

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
    # Render 환경변수 우선, 없으면 DB 확인
    env_key = os.getenv(service.upper() + "_KEY")
    if env_key:
        return env_key
    cur.execute("SELECT api_key FROM keys WHERE service = ?", (service,))
    row = cur.fetchone()
    return row[0] if row else None

@bot.event
async def on_ready():
    await tree.sync()
    print(f"봇 로그인 완료: {bot.user}")

@tree.command(name="ping", description="봇의 핑 확인")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@tree.command(name="restart", description="봇 재시작 (개발자만 가능)")
async def restart(interaction: discord.Interaction):
    if interaction.user.id != 909360134566862878:
        await interaction.response.send_message("이 명령어는 개발자만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message("봇을 재시작합니다...", ephemeral=True)
    os._exit(1)

@tree.command(name="serverinfo", description="서버 정보를 표시합니다.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, description="서버 정보", color=discord.Color.blue())
    embed.add_field(name="멤버 수", value=guild.member_count)
    embed.add_field(name="서버 ID", value=guild.id)
    embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo", description="유저 정보를 표시합니다.")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user}", color=discord.Color.green())
    embed.add_field(name="유저 ID", value=user.id)
    embed.add_field(name="계정 생성일", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="서버 참가일", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    await interaction.response.send_message(embed=embed)

@tree.command(name="weather", description="날씨를 확인합니다.")
async def weather(interaction: discord.Interaction, city: str):
    key = await get_api_key("weather")
    if not key:
        await interaction.response.send_message("WeatherAPI 키가 설정되지 않았습니다.", ephemeral=True)
        return
    async with aiohttp.ClientSession() as session:
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}"
        async with session.get(url) as resp:
            if resp.status != 200:
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
                await interaction.followup.send("GPT 요청 실패")
                return
            data = await resp.json()
            answer = data["choices"][0]["message"]["content"]
            await interaction.followup.send(answer)

bot.run(os.getenv("DISCORD_TOKEN"))