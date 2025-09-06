import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="사용 가능한 명령어 목록을 보여줍니다.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📌 명령어 목록", color=discord.Color.green())
        embed.add_field(name="/userinfo [유저]", value="유저 정보 확인", inline=False)
        embed.add_field(name="/loglookup [내용]", value="로그 검색", inline=False)
        embed.add_field(name="/schedule", value="예약 확인/추가", inline=False)
        embed.add_field(name="/patchnote", value="패치노트 확인", inline=False)
        embed.add_field(name="/support [내용]", value="고객지원 요청 등록", inline=False)
        embed.add_field(name="/accordingtobot", value="따까리봇 설명", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
