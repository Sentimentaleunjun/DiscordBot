import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TOKEN = os.getenv("DISCORD_TOKEN")
DEVELOPER_ID = 909360134566862878

bot = commands.Bot(command_prefix="!", intents=intents)

def init_db():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        guild_id TEXT,
        service TEXT,
        key TEXT,
        PRIMARY KEY (guild_id, service)
    )
    """)
    conn.commit()
    conn.close()

def set_api_key(guild_id, service, key):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO api_keys (guild_id, service, key)
    VALUES (?, ?, ?)
    """, (str(guild_id), service, key))
    conn.commit()
    conn.close()

def get_api_key(guild_id, service):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM api_keys WHERE guild_id=? AND service=?", (str(guild_id), service))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

@bot.event
async def on_ready():
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f"명령어 {len(synced)}개 동기화 완료")
    except Exception as e:
        print(f"동기화 실패: {e}")
    print(f"{bot.user} 로 로그인됨")

@bot.tree.command(name="ping", description="봇의 핑을 확인")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="restart", description="봇을 재시작 (개발자만)")
async def restart(interaction: discord.Interaction):
    if interaction.user.id != DEVELOPER_ID:
        await interaction.response.send_message("이 명령어는 개발자만 실행할 수 있습니다.", ephemeral=True)
        return
    await interaction.response.send_message("봇을 재시작합니다...", ephemeral=True)
    await bot.close()

@bot.tree.command(name="setkey", description="API 키를 저장 (서버 관리자만)")
@app_commands.describe(service="서비스 이름", key="API 키")
async def setkey(interaction: discord.Interaction, service: str, key: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    set_api_key(interaction.guild.id, service, key)
    await interaction.response.send_message(f"{service} API 키가 저장되었습니다.", ephemeral=True)

@bot.tree.command(name="getkey", description="저장된 API 키 조회 (서버 관리자만)")
@app_commands.describe(service="서비스 이름")
async def getkey(interaction: discord.Interaction, service: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    key = get_api_key(interaction.guild.id, service)
    if key:
        await interaction.response.send_message(f"{service} API 키: `{key}`", ephemeral=True)
    else:
        await interaction.response.send_message(f"{service} API 키가 없습니다.", ephemeral=True)

@bot.tree.command(name="dblookup", description="DB 내용 확인 (서버 관리자만)")
async def dblookup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("이 명령어는 서버 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT guild_id, service FROM api_keys")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        await interaction.response.send_message("DB에 저장된 API 키가 없습니다.", ephemeral=True)
    else:
        msg = "\n".join([f"서버: {r[0]} | 서비스: {r[1]}" for r in rows])
        await interaction.response.send_message(f"저장된 키 목록:\n{msg}", ephemeral=True)


bot.run(TOKEN)