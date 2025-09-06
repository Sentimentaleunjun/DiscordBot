import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

# 네 개발자 ID
DEVELOPER_ID = 909360134566862878

class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="support", description="따까리봇 개발자에게 문의/피드백을 보냅니다.")
    async def support(self, interaction: discord.Interaction, message: str):
        db.add_support(str(interaction.user.id), message)
        await interaction.response.send_message("✅ 문의가 등록되었습니다!", ephemeral=True)

    @app_commands.command(name="supportlist", description="등록된 문의 목록을 확인 (개발자 전용)")
    async def supportlist(self, interaction: discord.Interaction):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 이 명령어는 개발자 전용입니다.", ephemeral=True)
            return

        rows = db.get_supports()
        if not rows:
            await interaction.response.send_message("📭 아직 등록된 문의가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(title="📋 따까리봇 문의 리스트", color=discord.Color.green())
        for r in rows:
            status = "🟢 열림" if r[3] == "open" else "🔴 닫힘"
            embed.add_field(
                name=f"ID {r[0]} - User {r[1]} [{status}]",
                value=f"{r[2]} ({r[4]})",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="supportclose", description="특정 문의를 닫습니다 (개발자 전용)")
    async def supportclose(self, interaction: discord.Interaction, support_id: int):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 이 명령어는 개발자 전용입니다.", ephemeral=True)
            return

        success = db.close_support(support_id)
        if success:
            await interaction.response.send_message(f"✅ ID {support_id} 문의가 닫혔습니다.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ ID {support_id} 문의를 찾을 수 없습니다.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Support(bot))
