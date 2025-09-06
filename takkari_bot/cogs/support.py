import discord
from discord import app_commands
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="support", description="서포트를 등록합니다.")
    async def support(self, interaction: discord.Interaction, content: str):
        await interaction.response.send_message(f"✅ 서포트 등록됨: {content}")

async def setup(bot):
    await bot.add_cog(Support(bot))
