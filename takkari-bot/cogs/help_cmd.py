import discord
from discord.ext import commands

class HelpCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="따까리봇 도움말")
    async def help(self, ctx):
        embed = discord.Embed(
            title="📌 따까리봇 도움말",
            description="안녕하세요! **따까리봇**입니다. 아래 명령어를 참고하세요!",
            color=discord.Color.blue()
        )
        embed.add_field(name="/help", value="도움말을 확인합니다.", inline=False)
        embed.add_field(name="/dblookup", value="서버 관리자가 DB를 조회합니다.", inline=False)
        embed.add_field(name="/patchnote", value="패치노트를 확인합니다.", inline=False)
        embed.add_field(name="/support [내용]", value="고객지원 문의를 등록합니다.", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCmd(bot))
