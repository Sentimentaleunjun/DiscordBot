import discord
from discord import app_commands
from discord.ext import tasks
from flask import Flask
import os
import threading
from itertools import cycle

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

# ===== 추가: 상태 메시지 변경 =====
status_messages = cycle([
    "/help 입력해보세요!",
    "서버 관리 중 🔧",
    "GSEJ Company Beta v0.5"
])

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.CustomActivity(next(status_messages)))
# =================================


@client.tree.command(name="help", description="따까리 봇 도움말")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 도움말",
        description="안녕하세요! **여러분들의 디스코드를 더욱 편리하게 바꿔줄 잡일해결봇 따까리봇 입니다**.\n\n",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="따까리봇 도움말을 확인합니다", inline=False)
    embed.add_field(name="✅ `/accordingtobot [message]`", value="서버에 공지를 전송합니다 (관리자 전용), 반드시 '공지' 채널에서만 작동", inline=False)
    embed.add_field(name="✅ `/ping`", value="봇의 지연시간을 확인합니다", inline=False)
    embed.add_field(name="✅ `/userinfo [@유저]`", value="해당 유저의 정보를 확인합니다", inline=False)
    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    embed.set_footer(text="앞으로 더 많은 기능이 추가됩니다 🚀 | Edited by GSEJ Company . This is beta version")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))

    await interaction.response.defer(ephemeral=False)  # 응답 지연 방지
    await interaction.followup.send(embed=embed, view=view)


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


# ===== 추가: Ping 명령어 =====
@client.tree.command(name="ping", description="봇의 지연시간을 확인합니다")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)  # ms 단위
    await interaction.response.send_message(f"🏓 퐁! 현재 지연시간: **{latency}ms**")
# =================================


# ===== 추가: Userinfo 명령어 =====
@client.tree.command(name="userinfo", description="유저 정보를 확인합니다")
@app_commands.describe(user="정보를 확인할 유저를 선택하세요")
async def userinfo(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    embed = discord.Embed(title="👤 유저 정보", color=discord.Color.green())
    embed.add_field(name="닉네임", value=user.name, inline=True)
    embed.add_field(name="디스코드 태그", value=user.discriminator, inline=True)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)
# =================================


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
    change_status.start()
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


# Flask Web
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


