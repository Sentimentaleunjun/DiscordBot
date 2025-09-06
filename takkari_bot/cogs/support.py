import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="support", description="고객 지원 요청을 남깁니다.")
    async def support(self, interaction: discord.Interaction, message: str):
        db.add_support(str(interaction.user.id), message)
        await interaction.response.send_message("✅ 지원 요청이 접수되었습니다.", ephemeral=True)

    @app_commands.command(name="supportlist", description="저장된 고객 지원 요청 목록을 확인합니다.")
    async def supportlist(self, interaction: discord.Interaction):
        rows = db.get_supports()

        if not rows:
            await interaction.response.send_message("📭 저장된 고객 지원 요청이 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(title="📋 고객 지원 요청 목록", color=discord.Color.green())
        for r in rows:
            # r은 튜플: (id, user_id, message, created_at)
            embed.add_field(
                name=f"ID {r[0]} - User {r[1]}",
                value=f"{r[2]} (📅 {r[3]})",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))
