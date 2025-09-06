import discord
from discord import app_commands
from discord.ext import commands

class LogLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loglookup", description="서버 로그를 조회합니다.")
    async def loglookup(self, interaction: discord.Interaction):
        await interaction.response.send_message("📜 최근 로그 없음")

async def setup(bot):
    await bot.add_cog(LogLookup(bot))
