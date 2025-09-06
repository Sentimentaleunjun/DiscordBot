import discord
from discord.ext import commands
from discord import app_commands

class AccordingToBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="accordingtobot", description="따까리봇 설명")
    async def accordingtobot(self, interaction: discord.Interaction):
        await interaction.response.send_message("🤖 따까리봇은 서버 관리를 도와주는 디스코드 봇입니다!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AccordingToBot(bot))
