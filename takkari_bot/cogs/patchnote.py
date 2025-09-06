import discord
from discord import app_commands
from discord.ext import commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="patchnote", description="패치노트를 확인합니다.")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(title="패치노트", description="최근 업데이트 내역 없음.", color=0x00ffcc)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
