# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="지원")
    async def support(self, ctx, *, message: str):
        """지원 메시지 남기기"""
        embed = discord.Embed(
            title="📩 고객지원",
            description=message,
            color=0x3399ff
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SupportCog(bot))
