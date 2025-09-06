import discord
from discord import app_commands
from discord.ext import commands

class AccordingToBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="according_to_bot", description="봇 상태를 확인합니다.")
    async def according_to_bot(self, interaction: discord.Interaction):
        await interaction.response.send_message("🤖 봇이 정상적으로 동작 중입니다!")

async def setup(bot):
    await bot.add_cog(AccordingToBot(bot))
