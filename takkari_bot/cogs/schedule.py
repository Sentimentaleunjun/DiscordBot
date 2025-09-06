import discord
from discord import app_commands
from discord.ext import commands

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="schedule", description="스케줄을 확인합니다.")
    async def schedule(self, interaction: discord.Interaction):
        await interaction.response.send_message("📅 등록된 스케줄 없음")

async def setup(bot):
    await bot.add_cog(Schedule(bot))
