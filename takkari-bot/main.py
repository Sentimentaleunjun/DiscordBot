import discord
from discord import app_commands
from flask import Flask
import os
import threading

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
    embed.add_field(name="✅ `/accordingtobot [message]`", value="서버에 공지를 전송합니다 (관리자 전용), 반드시 '공지' 채널에서만 작동", inline=False)
    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
    embed.set_footer(text="앞으로 더 많은 기능이 추가될 예정이에요 🚀")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))

    await interaction.response.send_message(embed=embed, view=view)

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


app = Flask("")

@app.route("/")
def home():
    return "따까리봇 웹서버가 정상 작동 중입니다!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

client.run(os.environ["DISCORD_TOKEN"])
