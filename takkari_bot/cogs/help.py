import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="명령어 도움말을 확인합니다.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="도움말", description="사용 가능한 명령어 목록입니다.", color=0x00ffcc)
        embed.add_field(name="/support", value="서포트를 등록합니다.", inline=False)
        embed.add_field(name="/schedule", value="스케줄을 확인합니다.", inline=False)
        embed.add_field(name="/patchnote", value="패치노트를 확인합니다.", inline=False)
        embed.add_field(name="/db_lookup", value="DB를 조회합니다.", inline=False)
        embed.add_field(name="/according_to_bot", value="봇 상태 확인", inline=False)
        embed.add_field(name="/userinfo", value="유저 정보를 확인합니다.", inline=False)
        embed.add_field(name="/loglookup", value="로그를 조회합니다.", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
