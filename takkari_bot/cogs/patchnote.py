import discord
from discord.ext import commands
from discord import app_commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = [
            "🎉 따까리봇 1.0.13",
            "📅 출시일: 2025-09-10",
            "🛠 버그 수정 및 안정성 강화",
            "⚡ 에러 핸들링 강화 및 UI/UX 개선",
            "🔧 코그 구조 최적화 및 통합",
            "💖 사용자 편의성 향상: 명령어 반응 개선 및 피드백 반영"
        ]

    @app_commands.command(name="patchnote", description="따까리봇 패치노트를 확인합니다 📌")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📢패치노트",
            description="\n".join(self.notes),
            color=discord.Color.purple()
        )
        embed.set_footer(text="Edited by Flow in GSEJ 💖")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
