import discord
from discord import app_commands
import sqlite3
import os, sys

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    guild_id TEXT,
    service TEXT,
    key TEXT,
    PRIMARY KEY (guild_id, service)
)
""")

db.commit()

def is_server_admin(interaction: discord.Interaction):
    return interaction.user.guild_permissions.administrator

def get_api_key(guild_id: int, service: str):
    cursor.execute("SELECT key FROM api_keys WHERE guild_id = ? AND service = ?", (str(guild_id), service))
    row = cursor.fetchone()
    return row[0] if row else None

@client.event
async def on_ready():
    await tree.sync()
    print(f"봇 로그인 완료: {client.user}")

@tree.command(name="ping", description="핑 확인")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 퐁! {round(client.latency * 1000)}ms")

@tree.command(name="restart", description="봇 재시작 (개발자 전용)")
async def restart(interaction: discord.Interaction):
    if interaction.user.id != 909360134566862878:
        await interaction.response.send_message("❌ 이 명령어는 봇 개발자만 사용할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message("♻️ 봇이 재시작됩니다.", ephemeral=True)
    cursor.execute("INSERT INTO logs(user, action) VALUES(?, ?)", (interaction.user.name, "봇 재시작"))
    db.commit()
    os.execv(sys.executable, ['python'] + sys.argv)

@tree.command(name="serverinfo", description="서버 정보를 확인합니다")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="서버 정보", color=discord.Color.blue())
    embed.add_field(name="서버 이름", value=guild.name, inline=False)
    embed.add_field(name="서버 ID", value=guild.id, inline=False)
    embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="userlookup", description="유저 정보를 조회 (관리자 전용)")
async def userlookup(interaction: discord.Interaction, user: discord.User):
    if not is_server_admin(interaction):
        await interaction.response.send_message("❌ 이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    embed = discord.Embed(title="유저 정보", color=discord.Color.green())
    embed.add_field(name="이름", value=user.name, inline=False)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="봇 여부", value=user.bot, inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="loglookup", description="로그를 확인 (관리자 전용)")
async def loglookup(interaction: discord.Interaction, limit: int = 10):
    if not is_server_admin(interaction):
        await interaction.response.send_message("❌ 이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    cursor.execute("SELECT user, action, timestamp FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    if not rows:
        await interaction.response.send_message("📂 로그가 없습니다.", ephemeral=True)
        return
    log_text = "\n".join([f"[{r[2]}] {r[0]}: {r[1]}" for r in rows])
    await interaction.response.send_message(f"**최근 {limit}개의 로그**\n{log_text}")

@tree.command(name="dblookup", description="DB 데이터를 조회 (관리자 전용)")
async def dblookup(interaction: discord.Interaction):
    if not is_server_admin(interaction):
        await interaction.response.send_message("❌ 이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    cursor.execute("SELECT username, data, timestamp FROM users ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    if not rows:
        await interaction.response.send_message("📂 DB에 저장된 데이터가 없습니다.", ephemeral=True)
        return
    db_text = "\n".join([f"[{r[2]}] {r[0]}: {r[1]}" for r in rows])
    await interaction.response.send_message(f"**최근 데이터**\n{db_text}")

@tree.command(name="setkey", description="API 키를 설정 (관리자 전용)")
async def setkey(interaction: discord.Interaction, service: str, key: str):
    if not is_server_admin(interaction):
        await interaction.response.send_message("❌ 이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    cursor.execute("INSERT OR REPLACE INTO api_keys(guild_id, service, key) VALUES(?, ?, ?)", (str(interaction.guild_id), service, key))
    db.commit()
    await interaction.response.send_message(f"🔑 `{service}` API 키가 저장되었습니다.", ephemeral=True)

@tree.command(name="getkey", description="저장된 API 키 확인 (관리자 전용)")
async def getkey(interaction: discord.Interaction, service: str):
    if not is_server_admin(interaction):
        await interaction.response.send_message("❌ 이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    key = get_api_key(interaction.guild_id, service)
    if not key:
        await interaction.response.send_message(f"❌ `{service}` 키가 등록되지 않았습니다.", ephemeral=True)
    else:
        await interaction.response.send_message(f"🔑 `{service}` 키: `{key}`", ephemeral=True)

client.run(os.environ["DISCORD_TOKEN"])