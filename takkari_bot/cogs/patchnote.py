# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class PatchnoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="패치노트")
    async def patchnote(self, ctx):
        embed = discord.Embed(
            title="📜 패치노트",
            description="최근 업데이트 내역입니다.",
            color=0x66ff66
        )
        embed.add_field(name="v1.0.0", value="- 따까리봇 최초 출시", inline=False)
        embed.add_field(name="v1.1.0", value="- 공지, 예약공지 기능 추가", inline=False)
        embed.add_field(name="v1.2.0", value="- DB 조회, 지원 기능 추가", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchnoteCog(bot))
