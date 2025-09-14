import discord
from discord.ext import commands
from discord import app_commands

class AddSchedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedules = []

    @app_commands.command(name="addschedule", description="스케줄을 추가합니다 💘")
    async def addschedule(self, interaction: discord.Interaction, schedule: str):
        self.schedules.append(schedule)
        await interaction.response.send_message(f"✅ 스케줄 '{schedule}'이 추가되었습니다.", ephemeral=True)

    @app_commands.command(name="viewschedules", description="모든 스케줄을 조회합니다 💘")
    async def viewschedules(self, interaction: discord.Interaction):
        if not self.schedules:
            await interaction.response.send_message("스케줄이 없습니다.", ephemeral=True)
            return
        desc = "\n".join(self.schedules)
        await interaction.response.send_message(f"```{desc}```", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddSchedule(bot))
