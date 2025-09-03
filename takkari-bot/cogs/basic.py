import discord
from discord import app_commands
from discord.ext import commands
import os

DEV_ID = 909360134566862878

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="핑을 확인합니다")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency*1000)}ms")

    @app_commands.command(name="restart", description="봇을 재시작합니다 (개발자 전용)")
    async def restart(self, interaction: discord.Interaction):
        if interaction.user.id != DEV_ID:
            await interaction.response.send_message("❌ 개발자만 사용할 수 있습니다.", ephemeral=True)
            return
        await interaction.response.send_message("♻️ 봇을 재시작합니다...", ephemeral=True)
        os._exit(0)

async def setup(bot):
    await bot.add_cog(Basic(bot))
