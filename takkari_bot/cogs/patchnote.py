# patchnote.py
import discord
from discord.ext import commands
from discord import app_commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = ["v0.8 베타 시작!", "유저 정보 기능 추가"]

    @app_commands.command(name="patchnote", description="최근 패치노트를 확인합니다.")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📢 패치노트", description="\n".join(self.notes), color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
