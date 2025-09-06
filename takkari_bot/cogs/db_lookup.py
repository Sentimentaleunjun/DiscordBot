# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from takkari_bot.utils.db import get_supports

class DBLookupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="지원목록")
    async def lookup(self, ctx):
        """DB에서 지원자 목록 불러오기"""
        supports = get_supports()
        if not supports:
            await ctx.send("지원자가 없습니다.")
            return
        embed = discord.Embed(
            title="지원자 목록",
            description="\n".join(supports),
            color=0xffcc00
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DBLookupCog(bot))
