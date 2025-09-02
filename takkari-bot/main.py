import discord
from discord import app_commands
from flask import Flask
import os
import threading
import asyncio
from datetime import datetime


OWNER_ID = 909360134566862878

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

@client.tree.command(name="help", description="따까리 봇 도움말")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 도움말",
        description="안녕하세요! **여러분들의 디스코드를 더욱 편리하게 바꿔줄 잡일해결봇 따까리봇 입니다**.\n\n",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="따까리봇 도움말을 확인합니다", inline=False)
    embed.add_field(name="✅ `/accordingtobot [message]`", value="서버에 공지를 전송합니다 (관리자 전용)", inline=False)
    embed.add_field(name="✅ `/restart`", value="봇을 재시작합니다 (봇 소유자 전용)", inline=False)
    embed.add_field(name="✅ `/ping`", value="봇 지연 속도를 확인합니다", inline=False)
    embed.add_field(name="✅ `/serverinfo`", value="서버 정보를 확인합니다", inline=False)
    embed.add_field(name="✅ `/userinfo [유저]`", value="유저 정보를 확인합니다", inline=False)
    embed.add_field(name="✅ `/schedule_announcement [분] [메시지]`", value="지정 시간 후 공지를 보냅니다 (관리자 전용)", inline=False)
    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    embed.set_footer(text="앞으로 더 많은 기능이 추가됩니다 🚀 | Edited by GSEJ Company . This is beta version")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

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

async def welcome_member(member):
    channel = discord.utils.get(member.guild.text_channels, name="환영합니다")
    role = discord.utils.get(member.guild.roles, name="회원")
    if channel:
        await channel.send(f"🎉 환영합니다 {member.mention}님! 서버에 오신 걸 환영해요 👋")
    if role and not (member.bot or member.guild_permissions.administrator):
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print(f"⚠️ {member}에게 역할을 부여할 권한이 없습니다.")
    client.welcomed_members.add(member.id)

@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    print(f"✅ 봇 로그인 완료: {client.user} (ID: {client.user.id})")
    for guild in client.guilds:
        for member in guild.members:
            if not member.bot and member.status != discord.Status.offline:
                if member.id not in client.welcomed_members:
                    await welcome_member(member)

@client.event
async def on_member_join(member):
    await welcome_member(member)

@client.event
async def on_presence_update(before, after):
    if after.status != discord.Status.offline and after.id not in client.welcomed_members:
        await welcome_member(after)


# --- /restart 명령어 추가 ---
class RestartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label="예, 재시작합니다", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ 이 버튼은 봇 소유자만 사용할 수 있습니다.", ephemeral=True)
            return
        await interaction.response.send_message("♻️ 봇이 곧 재시작됩니다...", ephemeral=True)
        await interaction.client.close()
        os._exit(0)

    @discord.ui.button(label="아니오, 취소합니다", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ 이 버튼은 봇 소유자만 사용할 수 있습니다.", ephemeral=True)
            return
        await interaction.response.send_message("✅ 재시작이 취소되었습니다.", ephemeral=True)
        self.stop()

@client.tree.command(name="restart", description="따까리봇을 재시작합니다 (봇 소유자 전용)")
async def restart(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ 이 명령어는 봇 소유자만 사용할 수 있습니다.", ephemeral=True)
        return
    view = RestartView()
    await interaction.response.send_message(
        "⚠️ **정말로 봇을 재시작하시겠습니까?**",
        view=view,
        ephemeral=True
    )

# --- /ping 명령어 ---
@client.tree.command(name="ping", description="봇 지연 속도를 확인합니다")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"🏓 퐁! 현재 지연 속도: **{latency}ms**", ephemeral=True)

# --- /serverinfo 명령어 ---
@client.tree.command(name="serverinfo", description="서버 정보를 확인합니다")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="서버 정보", color=discord.Color.green())
    embed.add_field(name="서버 이름", value=guild.name, inline=False)
    embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
    embed.add_field(name="역할 수", value=len(guild.roles), inline=False)
    embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# --- /userinfo 명령어 ---
@client.tree.command(name="userinfo", description="유저 정보를 확인합니다")
@app_commands.describe(user="정보를 확인할 유저 (비워두면 자기 자신)")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user.name}님의 정보", color=discord.Color.purple())
    embed.add_field(name="닉네임", value=user.display_name, inline=False)
    embed.add_field(name="가입일", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="계정 생성일", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# --- /schedule_announcement 명령어 ---
@client.tree.command(name="schedule_announcement", description="일정 시간 후 공지를 보냅니다 (관리자 전용)")
@app_commands.describe(minutes="몇 분 후 보낼지", message="공지 내용")
async def schedule_announcement(interaction: discord.Interaction, minutes: int, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message(f"⏳ {minutes}분 후 공지가 전송됩니다.", ephemeral=True)
    await asyncio.sleep(minutes * 60)
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel:
        await channel.send(f"⏰ 예약 공지: {message}")

# Flask 웹서버
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
