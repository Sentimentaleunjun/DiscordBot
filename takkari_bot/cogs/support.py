import discord
from discord.ext import commands
from discord import app_commands
from takkari_bot.utils import db

DEVELOPER_ID = 909360134566862878

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot = bot

    @app_commands.command(name="support", description="문의/피드백 등록")
    async def support(self, interaction: discord.Interaction, message: str):
        try:
            db.add_support(str(interaction.user.id), message)
            await interaction.response.send_message("✅ 문의가 등록되었습니다!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(name="supportlist", description="등록된 문의 확인 (개발자 전용)")
    async def supportlist(self, interaction: discord.Interaction):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 개발자 전용입니다.", ephemeral=True)
            return
        rows = db.get_supports()
        if not rows:
            await interaction.response.send_message("📭 문의가 없습니다.", ephemeral=True)
            return
        embed = discord.Embed(title="📋 문의 리스트", color=discord.Color.green())
        for r in rows:
            status = "🟢 열림" if r[3] == "open" else "🔴 닫힘"
            embed.add_field(
                name=f"ID {r[0]} - User {r[1]} [{status}]",
                value=f"{r[2]} ({r[4]})",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="supportclose", description="문의 닫기 (개발자 전용)")
    async def supportclose(self, interaction: discord.Interaction, support_id: int):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 개발자 전용입니다.", ephemeral=True)
            return
        user_id = db.close_support(support_id)
        if not user_id:
            await interaction.response.send_message("⚠️ 문의를 찾을 수 없거나 이미 닫힘", ephemeral=True)
            return
        # 닫힘 알림을 문의 등록자에게 DM 전송
        user = await self.bot.fetch_user(int(user_id))
        try:
            await user.send(f"✅ 문의 ID {support_id}가 닫혔습니다.")
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"✅ ID {support_id} 문의가 닫혔습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))
