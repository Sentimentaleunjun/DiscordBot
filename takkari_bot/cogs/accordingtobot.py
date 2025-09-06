# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class AccordingToBotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="따까리봇")
    async def info(self, ctx):
        embed = discord.Embed(
            title="따까리봇 정보",
            description="나는 주인님의 충직한 따까리봇입니다 🤖",
            color=0xff66cc
        )
        embed.add_field(name="기능", value="공지, 예약, 지원, 패치노트, DB 조회", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AccordingToBotCog(bot))
