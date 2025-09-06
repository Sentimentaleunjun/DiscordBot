import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="봇의 모든 명령어를 확인합니다.")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📖 도움말", color=discord.Color.blue())
        embed.add_field(name="/support", value="고객 지원 요청 남기기", inline=False)
        embed.add_field(name="/supportlist", value="저장된 고객 지원 목록 보기", inline=False)
        embed.add_field(name="/userinfo", value="유저 정보 확인", inline=False)
        embed.add_field(name="/loglookup", value="로그 검색 기능", inline=False)
        embed.add_field(name="/patchnote", value="패치노트 확인", inline=False)
        embed.add_field(name="/schedule", value="일정 관리", inline=False)
        embed.add_field(name="/announce", value="공지 전송 (관리자용)", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
