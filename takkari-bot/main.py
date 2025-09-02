import discord
from discord import app_commands
from flask import Flask
import os
import threading
import datetime
import sys

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

client = MyClient()

# 로그 기록 함수
def log_event(message: str):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("bot.log", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

@client.tree.command(name="help", description="따까리 봇 도움말")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 도움말",
        description="안녕하세요! **여러분들의 디스코드를 더욱 편리하게 바꿔줄 잡일해결봇 따까리봇 입니다**.\n\n",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="따까리봇 도움말을 확인합니다", inline=False)
    embed.add_field(name="✅ `/accordingtobot [message]`", value="서버에 공지를 전송합니다 (관리자 전용), 반드시 '공지' 채널에서만 작동", inline=False)
    embed.add_field(name="✅ `/restart`", value="봇을 재시작합니다 (관리자 전용)", inline=False)
    embed.add_field(name="✅ `/loglookup`", value="봇의 최근 로그를 확인합니다 (관리자 전용)", inline=False)
    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    embed.set_footer(text="앞으로 더 많은 기능이 추가됩니다 🚀 | Edited by GSEJ Company . This is beta version")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    log_event(f"/help 명령어 실행 by {interaction.user} ({interaction.user.id})")

@client.tree.command(name="accordingtobot", description="서버에 공지를 전송합니다 (관리자 전용)")
@app_commands.describe(message="전송할 공지 내용을 입력하세요")
async def accordingtobot(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        log_event(f"/accordingtobot 권한 없음 by {interaction.user} ({interaction.user.id})")
        return
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel is None:
        await interaction.response.send_message("❌ 공지 채널을 찾을 수 없습니다.", ephemeral=True)
        log_event(f"/accordingtobot 공지 채널 없음 by {interaction.user} ({interaction.user.id})")
        return
    await channel.send(f"📢 서버 공지사항: {message}")
    await interaction.response.send_message(f"✅ 공지가 {channel.mention} 채널에 전송되었습니다.", ephemeral=True)
    log_event(f"/accordingtobot 공지 전송 by {interaction.user} ({interaction.user.id}) 내용: {message}")

@client.tree.command(name="restart", description="봇을 재시작합니다 (관리자 전용)")
async def restart(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        log_event(f"/restart 권한 없음 by {interaction.user} ({interaction.user.id})")
        return
    await interaction.response.send_message("♻️ 봇을 재시작합니다...", ephemeral=True)
    log_event(f"/restart 명령어 실행 by {interaction.user} ({interaction.user.id})")
    os.execv(sys.executable, ['python'] + sys.argv)

@client.tree.command(name="loglookup", description="봇의 최근 로그를 확인합니다 (관리자 전용)")
async def loglookup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        log_event(f"/loglookup 권한 없음 by {interaction.user} ({interaction.user.id})")
        return
    try:
        with open("bot.log", "r", encoding="utf-8") as f:
            logs = f.readlines()[-10:]  # 최근 10줄
        content = "```\n" + "".join(logs) + "\n```"
    except FileNotFoundError:
        content = "아직 로그 파일이 없습니다."
    await interaction.response.send_message(content, ephemeral=True)
    log_event(f"/loglookup 명령어 실행 by {interaction.user} ({interaction.user.id})")

@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    log_event(f"봇 로그인 완료: {client.user} (ID: {client.user.id})")

# Flask 서버
app = Flask("")

@app.route("/")
def home():
    return "따까리봇 웹서버가 정상 작동 중입니다! 따까리봇 디스코드 봇 , Version 0.5 Betatest"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

client.run(os.environ["DISCORD_TOKEN"])
