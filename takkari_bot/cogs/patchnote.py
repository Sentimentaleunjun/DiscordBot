# takkari_bot/cogs/patchnote.py
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

DB_PATH = "db.sqlite"

# 운영진/제작자 역할 ID
ADMIN_ROLE_IDS = [1416769282380922991, 1416769872284876931]
# 패치노트 채널 ID
PATCH_CHANNEL_ID = 1417426181942153237

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()

    # DB 초기화
    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patchnotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    # -----------------------------
    # 운영진 전용: 패치노트 등록
    @app_commands.command(name="add_patchnote", description="운영진/제작자 전용: 패치노트 등록")
    async def add_patchnote(self, interaction: discord.Interaction, version: str, content: str):
        if not any(role.id in ADMIN_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message("❌ 이 명령어는 운영진/제작자 전용입니다.", ephemeral=True)
            return

        # DB에 저장
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patchnotes (version, content, author) VALUES (?, ?, ?)",
            (version, content, interaction.user.name)
        )
        conn.commit()
        conn.close()

        # 패치노트 채널에 전송
        channel = self.bot.get_channel(PATCH_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title=f"📢 패치노트 v{version}",
                description=content,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"등록자: {interaction.user.name}")
            await channel.send(embed=embed)

        await interaction.response.send_message(f"✅ 패치노트 v{version} 등록 완료", ephemeral=True)

    # -----------------------------
    # 누구나 패치노트 확인
    @app_commands.command(name="patchnote", description="최신 패치노트 확인")
    async def patchnote(self, interaction: discord.Interaction):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT version, content, author, created_at FROM patchnotes ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await interaction.response.send_message("❌ 등록된 패치노트가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(title="📜 최신 패치노트", color=discord.Color.blue())
        for row in rows:
            version, content, author, created_at = row
            embed.add_field(name=f"v{version} - {created_at}", value=f"{content}\n*등록자: {author}*", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))