import discord
from discord import app_commands
from discord.ext import commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="patchnote", description="📢 최신 패치노트를 확인합니다!")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📢 패치노트",
            description="따까리봇 **0.9.83 Final Beta** 출시!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="✨ 주요 변경사항",
            value=(
                "🌸 `/help` 이모티콘 & 귀여운 UI 업데이트\n"
                "🛠️ DB 기능 개선 및 안정화\n"
                "💌 DM 기능 일반 유저도 가능\n"
                "📑 정책 페이지와 연동 준비 완료\n"
            ),
            inline=False
        )
        embed.add_field(
            name="🚀 현황",
            value="정식 1.0 릴리즈 직전 단계! 마지막 베타 테스트 중입니다 💖",
            inline=False
        )
        embed.set_footer(text="GSEJ Company · 2025")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
