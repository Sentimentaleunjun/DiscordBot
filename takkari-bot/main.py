import discord
from discord import app_commands
from flask import Flask
import os
import threading
import logging
import asyncio
import datetime
import sys

# ===== 로그 설정 =====
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("bot.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Discord client
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False
        self.welcomed_members = set()

client = MyClient()
OWNER_ID = 909360134566862878

# ===== 명령어 =====
@client.tree.command(name="help", description="따까리 봇 도움말")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 도움말",
        description="따까리봇의 주요 기능 목록입니다.",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/ping`", value="봇의 지연 속도를 확인합니다.", inline=False)
    embed.add_field(name="✅ `/restart`", value="봇을 재시작합니다 (봇 주인만 가능).", inline=False)
    embed.add_field(name="✅ `/schedule`", value="서버 공지를 예약합니다 (관리자 전용).", inline=False)
    embed.add_field(name="✅ `/serverinfo`", value="서버 정보를 확인합니다.", inline=False)
    embed.add_field(name="✅ `/userinfo [유저]`", value="유저 정보를 확인합니다.", inline=False)
    embed.add_field(name="✅ `/loglookup`", value="최근 봇 로그를 확인합니다 (관리자 전용).", inline=False)
    embed.add_field(name="✅ `/accordingtobot [메시지]`", value="공지 채널에 공지를 전송합니다 (관리자 전용).", inline=False)
    embed.set_footer(text="Edited by GSEJ Company | This is beta version")

    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="ping", description="봇의 지연 속도를 확인합니다.")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! {latency}ms", ephemeral=True)
    logger.info(f"{interaction.user} ran /ping")

@client.tree.command(name="restart", description="봇을 재시작합니다 (봇 주인 전용)")
async def restart(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ 이 명령어는 봇 주인만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message("♻️ 봇을 재시작합니다...", ephemeral=True)
    logger.info(f"{interaction.user} ran /restart")
    await asyncio.sleep(1)
    os.execv(sys.executable, ["python"] + sys.argv)

@client.tree.command(name="accordingtobot", description="서버에 공지를 전송합니다 (관리자 전용)")
@app_commands.describe(message="전송할 공지 내용을 입력하세요")
async def accordingtobot(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel is None:
        await interaction.response.send_message("❌ 공지 채널을 찾을 수 없습니다.", ephemeral=True)
        return
    await channel.send(f"📢 서버 공지사항: {message}")
    await interaction.response.send_message(f"✅ 공지가 {channel.mention} 채널에 전송되었습니다.", ephemeral=True)
    logger.info(f"{interaction.user} ran /accordingtobot: {message}")

@client.tree.command(name="loglookup", description="최근 봇 로그를 확인합니다 (관리자 전용)")
async def loglookup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    try:
        with open("bot.log", "r", encoding="utf-8") as f:
            lines = f.readlines()[-20:]
        if not lines:
            await interaction.response.send_message("로그가 비어 있습니다.", ephemeral=True)
            return
        log_content = "```" + "".join(lines)[-1900:] + "```"
        await interaction.response.send_message(log_content, ephemeral=True)
    except FileNotFoundError:
        await interaction.response.send_message("로그 파일을 찾을 수 없습니다.", ephemeral=True)

@client.tree.command(name="schedule", description="공지 예약 (관리자 전용)")
@app_commands.describe(message="공지할 내용", minutes="몇 분 후에 공지?")
async def schedule(interaction: discord.Interaction, message: str, minutes: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"⏳ {minutes}분 후에 공지 전송 예약됨!", ephemeral=True)
    logger.info(f"{interaction.user} scheduled message: {message} after {minutes}min")
    await asyncio.sleep(minutes * 60)
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel:
        await channel.send(f"⏰ 예약된 공지: {message}")

@client.tree.command(name="serverinfo", description="서버 정보를 확인합니다.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild.name} 서버 정보", color=discord.Color.green())
    embed.add_field(name="서버 ID", value=guild.id, inline=False)
    embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
    embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="userinfo", description="유저 정보를 확인합니다.")
@app_commands.describe(user="정보를 볼 유저")
async def userinfo(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"{user.name} 유저 정보", color=discord.Color.purple())
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="가입일", value=user.joined_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="상태", value=str(user.status), inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ===== 환영 메시지 제거 + 역할만 부여 =====
async def welcome_member(member):
    role = discord.utils.get(member.guild.roles, name="회원")
    if role and not (member.bot or member.guild_permissions.administrator):
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print(f"⚠️ {member}에게 역할을 부여할 권한이 없습니다.")
    client.welcomed_members.add(member.id)
    logger.info(f"Welcomed member: {member.name} ({member.id})")

@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    print(f"✅ 봇 로그인 완료: {client.user} (ID: {client.user.id})")
    logger.info(f"Bot logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_member_join(member):
    await welcome_member(member)

@client.event
async def on_presence_update(before, after):
    if after.status != discord.Status.offline and after.id not in client.welcomed_members:
        await welcome_member(after)

# ===== Flask 웹 서버 =====
app = Flask("")

@app.route("/")
def home():
    return "따까리봇 웹서버가 정상 작동 중입니다! 따까리봇 디스코드 봇 , Version 0.6 Beta"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

client.run(os.environ["DISCORD_TOKEN"])

