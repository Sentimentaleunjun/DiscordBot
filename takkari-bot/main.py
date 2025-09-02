import discord
from discord import app_commands
from flask import Flask
import os
import threading
import logging
import sqlite3
from datetime import datetime

OWNER_ID = 909360134566862878
LOG_FILE = "bot.log"
DB_FILE = "bot.db"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS command_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                timestamp TEXT
            )""")
conn.commit()
conn.close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

client = MyClient()

def log_command(user_id, command):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO command_logs (user_id, command, timestamp) VALUES (?, ?, ?)",
              (user_id, command, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

@client.tree.command(name="help", description="따까리 봇 도움말")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 도움말",
        description="여러분의 디스코드를 편리하게! 따까리봇 입니다.\n",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="따까리봇 도움말", inline=False)
    embed.add_field(name="✅ `/accordingtobot`", value="공지 전송 (관리자)", inline=False)
    embed.add_field(name="✅ `/ping`", value="핑 속도", inline=False)
    embed.add_field(name="✅ `/restart`", value="봇 재시작 (봇주인)", inline=False)
    embed.add_field(name="✅ `/serverinfo`", value="서버 정보", inline=False)
    embed.add_field(name="✅ `/userinfo`", value="유저 정보", inline=False)
    embed.add_field(name="✅ `/dblookup`", value="DB 로그 조회 (봇주인)", inline=False)
    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    log_command(interaction.user.id, "/help")

@client.tree.command(name="accordingtobot", description="서버에 공지 전송 (관리자)")
@app_commands.describe(message="전송할 공지")
async def accordingtobot(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 가능", ephemeral=True)
        return
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel is None:
        await interaction.response.send_message("❌ 공지 채널 없음", ephemeral=True)
        return
    await channel.send(f"📢 서버 공지사항: {message}")
    await interaction.response.send_message(f"✅ 공지 완료: {channel.mention}", ephemeral=True)
    log_command(interaction.user.id, f"/accordingtobot {message}")

@client.tree.command(name="ping", description="핑 속도 확인")
async def ping_command(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"🏓 {latency}ms")
    log_command(interaction.user.id, "/ping")

@client.tree.command(name="restart", description="봇 재시작 (봇주인)")
async def restart_command(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ 봇 주인만 가능", ephemeral=True)
        return
    await interaction.response.send_message("♻️ 봇 재시작 중...", ephemeral=True)
    log_command(interaction.user.id, "/restart")
    await client.close()

@client.tree.command(name="serverinfo", description="서버 정보 확인")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"서버 정보 - {guild.name}", color=discord.Color.green())
    embed.add_field(name="서버 ID", value=guild.id, inline=False)
    embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
    embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else interaction.client.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    log_command(interaction.user.id, "/serverinfo")

@client.tree.command(name="userinfo", description="유저 정보 확인")
@app_commands.describe(member="조회할 유저")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"유저 정보 - {member.display_name}", color=discord.Color.orange())
    embed.add_field(name="유저 ID", value=member.id, inline=False)
    embed.add_field(name="계정 생성일", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="서버 가입일", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    log_command(interaction.user.id, f"/userinfo {member.id}")

@client.tree.command(name="dblookup", description="DB 로그 조회 (봇주인)")
@app_commands.describe(limit="가져올 로그 개수 (기본 10)")
async def dblookup(interaction: discord.Interaction, limit: int = 10):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ 봇 주인만 가능", ephemeral=True)
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, command, timestamp FROM command_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        await interaction.response.send_message("📂 저장된 로그가 없습니다.", ephemeral=True)
        return
    msg = "\n".join([f"👤 {r[0]} | {r[1]} | {r[2]}" for r in rows])
    await interaction.response.send_message(f"**최근 {len(rows)}개의 로그**\n{msg}", ephemeral=True)
    log_command(interaction.user.id, f"/dblookup {limit}")

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def start_flask():
    thread = threading.Thread(target=run_flask)
    thread.start()

@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    print(f"Logged in as {client.user}")

start_flask()
client.run(os.environ["DISCORD_TOKEN"])
