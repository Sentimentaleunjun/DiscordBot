import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="📖 도움말", description="사용 가능한 명령어 목록입니다.", color=0x00ffcc)
        embed.add_field(name="/help", value="도움말 확인", inline=False)
        embed.add_field(name="/patchnote", value="패치노트 확인/추가 (관리자만 추가 가능)", inline=False)
        embed.add_field(name="/support [내용]", value="고객지원 문의 등록", inline=False)
        embed.add_field(name="/dblookup", value="DB 조회 (관리자 전용)", inline=False)
        embed.add_field(name="/accordingtobot [내용]", value="공지 발송 (관리자 전용)", inline=False)
        embed.add_field(name="/schedule [YYYY-MM-DD HH:MM] [내용]", value="공지 예약 (관리자 전용)", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
