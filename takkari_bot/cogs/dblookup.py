# dblookup.py
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

DB_PATH = "db.sqlite"
ADMIN_ROLES = [1416769282380922991, 1416769872284876931]
RESULT_CHANNEL_ID = 1417052678378360914

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, member: discord.Member):
        return any(role.id in ADMIN_ROLES for role in member.roles)

    @app_commands.command(name="user_lookup", description="DB에서 유저 검색 (운영진 전용)")
    @app_commands.describe(query="유저 ID 또는 이름")
    async def user_lookup(self, interaction: discord.Interaction, query: str):
        if not self.is_admin(interaction.user):
            await interaction.response.send_message("❌ 당신은 이 명령어를 사용할 수 없습니다.", ephemeral=True)
            return

        # DB 조회
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE id=? OR name LIKE ?", (query, f"%{query}%"))
        results = cursor.fetchall()
        conn.close()

        if not results:
            await interaction.response.send_message("❌ 조회 결과가 없습니다.", ephemeral=True)
            return

        # 결과 메시지 생성
        message = "\n".join([f"ID: {r[0]}, 이름: {r[1]}" for r in results])
        channel = self.bot.get_channel(RESULT_CHANNEL_ID)
        if channel:
            await channel.send(f"DB 조회 결과:\n```{message}```")
        await interaction.response.send_message("✅ 조회 완료, 결과는 운영진 채널로 전송되었습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DBLookup(bot))