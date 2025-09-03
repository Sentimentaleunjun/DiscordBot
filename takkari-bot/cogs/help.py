import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇 도움말")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📌 따까리봇 도움말",
            description="안녕하세요! **여러분의 서버를 편리하게 바꿔줄 잡일해결봇, 따까리봇입니다!**\n\n"
                        "아래는 주요 명령어입니다:",
            color=discord.Color.blue()
        )
        embed.add_field(name="✅ `/help`", value="이 도움말을 확인합니다", inline=False)
        embed.add_field(name="✅ `/ping`", value="봇의 응답 속도를 확인합니다", inline=False)
        embed.add_field(name="✅ `/restart`", value="봇을 재시작합니다 (개발자 전용)", inline=False)
        embed.add_field(name="✅ `/serverinfo`", value="현재 서버 정보를 확인합니다", inline=False)
        embed.add_field(name="✅ `/userinfo [유저]`", value="특정 유저의 정보를 확인합니다", inline=False)
        embed.add_field(name="✅ `/dblookup`", value="DB를 조회합니다 (관리자 전용)", inline=False)
        embed.add_field(name="✅ `/loglookup`", value="봇 로그를 확인합니다 (관리자 전용)", inline=False)
        embed.add_field(name="✅ `/patchnotes`", value="패치노트를 조회/추가합니다", inline=False)
        embed.add_field(name="✅ `/support`", value="따까리봇 문의를 등록합니다", inline=False)

        embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
        embed.set_footer(text="앞으로 더 많은 기능이 추가됩니다 🚀")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))

