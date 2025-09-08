# takkari_bot/cogs/patchnote.py
import discord
from discord.ext import commands
from discord import app_commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = [
            "📢 따까리봇 0.9 Candidate Ver. 출시!",
            "✨ 주요 기능 업데이트",
            "🚀 공식 출시 임박, 베타테스트 시작!"
            "0.9.5 Codename : DePLayer (Final Beta) 개발 시작"
            "✨ 곧 1.0 으로 다시올게요!"
        ]

    @app_commands.command(name="patchnote", description="최근 패치노트를 확인합니다.")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📢 패치노트", description="\n".join(self.notes), color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
