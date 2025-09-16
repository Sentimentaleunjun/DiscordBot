import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

DB_PATH = "database.db"

# 운영진 역할 ID 목록
ADMIN_ROLE_IDS = [1416769282380922991, 1416769872284876931]

# 결과 전송 채널 ID
RESULT_CHANNEL_ID = 1417052678378360914


class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, member: discord.Member) -> bool:
        """운영진 역할 보유 여부 확인"""
        return any(role.id in ADMIN_ROLE_IDS for role in member.roles)

    @app_commands.command(name="dblookup", description="운영진 전용 DB 조회")
    async def dblookup(self, interaction: discord.Interaction, query: str):
        # 운영진 권한 체크
        if not self.is_admin(interaction.user):
            await interaction.response.send_message(
                "❌ 당신은 이 명령어를 사용할 수 없습니다.",
                ephemeral=True
            )
            return

        # 지연 방지: 처리 중 표시
        await interaction.response.defer(ephemeral=True)

        try:
            # DB 조회
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name FROM users WHERE id=? OR name LIKE ?",
                (query, f"%{query}%")
            )
            results = cursor.fetchall()
            conn.close()
        except Exception as e:
            await interaction.followup.send(f"❌ DB 조회 중 오류 발생: {e}", ephemeral=True)
            return

        # 결과 없을 때
        if not results:
            await interaction.followup.send("❌ 조회 결과가 없습니다.", ephemeral=True)
            return

        # 결과 문자열 정리
        message = "\n".join([f"ID: {r[0]}, 이름: {r[1]}" for r in results])

        # 운영진 전용 채널로 전송
        channel = self.bot.get_channel(RESULT_CHANNEL_ID)
        if channel:
            await channel.send(f"🔍 DB 조회 결과:\n```{message}```")

        # 최종 응답 (운영진만 볼 수 있음)
        await interaction.followup.send("✅ 조회 완료, 결과는 운영진 채널로 전송되었습니다.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(DBLookup(bot))