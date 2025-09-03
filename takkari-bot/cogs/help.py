import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇 도움말")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📌 따까리봇 도움말",
            description="안녕하세요! **여러분들의 디스코드를 더욱 편리하게 바꿔줄 잡일해결봇 따까리봇 입니다**.\n\n",
            color=discord.Color.blue()
        )
        embed.add_field(name="✅ `/help`", value="도움말을 확인합니다", inline=False)
        embed.add_field(name="✅ `/ping`", value="핑 확인", inline=False)
        embed.add_field(name="✅ `/restart`", value="봇 재시작 (개발자 전용)", inline=False)
        embed.add_field(name="✅ `/serverinfo`", value="서버 정보", inline=False)
        embed.add_field(name="✅ `/userinfo`", value="유저 정보", inline=False)
        embed.add_field(name="✅ `/dblookup`", value="DB 조회 (관리자)", inline=False)
        embed.add_field(name="✅ `/loglookup`", value="로그 조회 (관리자)", inline=False)
        embed.add_field(name="✅ `/patchnotes`", value="패치노트 등록/확인", inline=False)
        embed.add_field(name="✅ `/support`", value="고객 문의", inline=False)
        embed.set_thumbnail(url=interaction.client.user.display_avatar.url)
        embed.set_footer(text="앞으로 더 많은 기능이 추가됩니다 🚀 | GSEJ Company Beta Version")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
