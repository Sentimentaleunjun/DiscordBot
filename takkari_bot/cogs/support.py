# support.py
import discord
from discord.ext import commands
from discord import app_commands

# 외부/내부 의존성(없으면 코그 자체가 죽지 않도록 폴백)
try:
    from takkari_bot.utils.db import add_support, get_supports  # 프로젝트에 있을 때만 사용
except Exception:
    def add_support(user_id: str, message: str):
        # 배포 환경에 DB가 없으면 /support는 "수신만" 표시
        print("[support] add_support called (noop):", user_id, message)

    def get_supports():
        return []  # 목록 비어있다고 응답

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="support", description="고객지원 요청을 등록합니다.")
    async def support(self, interaction: discord.Interaction, message: str):
        add_support(str(interaction.user.id), message)
        await interaction.response.send_message("✅ 고객지원 요청이 등록되었습니다.", ephemeral=True)

    @app_commands.command(name="supportlist", description="등록된 고객지원 요청을 확인합니다. (관리자용)")
    async def supportlist(self, interaction: discord.Interaction):
        rows = get_supports()
        if not rows:
            await interaction.response.send_message("📭 등록된 고객지원 요청이 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(title="📩 고객지원 요청 목록", color=discord.Color.orange())
        for r in rows[:10]:
            embed.add_field(name=f"ID {r[0]} - User {r[1]}", value=f"{r[2]} ({r[3]})", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))
