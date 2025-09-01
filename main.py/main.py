import discord
from discord import app_commands
from flask import Flask
import os
import threading

# ----------------- Discord 봇 세팅 -----------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

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
        description="안녕하세요! 따까리봇입니다.",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="도움말 확인", inline=False)
    await interaction.response.send_message(embed=embed)

async def welcome_member(member):
    channel = discord.utils.get(member.guild.text_channels, name="환영합니다")
    role = discord.utils.get(member.guild.roles, name="회원")
    if channel:
        await channel.send(f"🎉 환영합니다 {member.mention}님!")
    if role and not (member.bot or member.guild_permissions.administrator):
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print(f"⚠️ {member}에게 역할 부여 불가.")
    client.welcomed_members.add(member.id)

@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    print(f"✅ 봇 로그인 완료: {client.user} (ID: {client.user.id})")

@client.event
async def on_member_join(member):
    await welcome_member(member)

# ----------------- Flask 웹 서버 -----------------
app = Flask(__name__)

@app.route("/")
def index():
    return "따까리봇 웹 서버가 실행 중입니다!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ----------------- 멀티 스레드 실행 -----------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    client.run(os.environ["DISCORD_TOKEN"])