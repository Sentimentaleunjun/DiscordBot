import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="📖 따까리봇 사용법을 확인해요!")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌸 따까리봇 도움말",
            description="✨ 따까리봇 0.9.83 Final Beta ✨\n\n귀여운 기능들을 확인해보세요!",
            color=discord.Color.pink()
        )
        embed.add_field(name="🛠️ /support", value="서포트 기능 확인 및 관리", inline=False)
        embed.add_field(name="💌 /dm", value="디엠 보내기 (관리자 전용/일반 유저용)", inline=False)
        embed.add_field(name="💰 /points", value="포인트 확인 및 추가", inline=False)
        embed.add_field(name="❓ /quiz", value="랜덤 퀴즈 도전!", inline=False)
        embed.add_field(name="📝 /userinfo", value="유저 정보 보기", inline=False)
        embed.add_field(name="📅 /schedule", value="일정 관리", inline=False)
        embed.add_field(name="📑 /patchnote", value="패치노트 확인", inline=False)

        embed.set_footer(text="따까리봇 © GSEJ Company 2025")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
