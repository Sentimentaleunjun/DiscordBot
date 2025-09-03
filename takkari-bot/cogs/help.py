import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(title="명령어 목록", color=discord.Color.blue())
        embed.add_field(name="/ping", value="따까리봇 핑 확인", inline=False)
        embed.add_field(name="/restart", value="봇 재시작 (개발자용)", inline=False)
        embed.add_field(name="/serverinfo", value="서버 정보 확인", inline=False)
        embed.add_field(name="/userinfo", value="유저 정보 확인", inline=False)
        embed.add_field(name="/loglookup", value="서버 로그 조회 (관리자용)", inline=False)
        embed.add_field(name="/dblookup", value="DB 조회 (관리자용)", inline=False)
        embed.add_field(name="/patchnotes", value="패치노트 확인", inline=False)
        embed.add_field(name="/support", value="고객지원 문의", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
