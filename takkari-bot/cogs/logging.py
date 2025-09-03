import discord
from discord import app_commands
from discord.ext import commands
import os

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loglookup", description="봇 로그를 확인합니다 (관리자 전용)")
    async def loglookup(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
            return

        if not os.path.exists("bot.log"):
            await interaction.response.send_message("⚠️ 로그 파일이 없습니다.", ephemeral=True)
            return

        with open("bot.log", "r", encoding="utf-8") as f:
            logs = f.read()[-1800:]  # 최근 로그 일부만
        await interaction.response.send_message(f"```{logs}```", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Logging(bot))
