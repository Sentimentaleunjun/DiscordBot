import discord
from discord.ext import commands
from discord import app_commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = [
            "📢 따까리봇 0.9.83 Final Beta 출시!",
            "✨ 스케줄/지원/DM/유저정보 슬래시 커맨드 통합",
            "🛠 안정성 강화 및 버그 수정",
            "🚀 서버 관리 상태 표시 개선"
        ]

    @app_commands.command(name="patchnote", description="최근 패치노트를 확인합니다.")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📢 패치노트", description="\n".join(self.notes), color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))