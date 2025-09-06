# takkari_bot/cogs/support.py
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from takkari_bot.utils.db import add_support

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="서포트")
    async def support_command(self, ctx, *, message: str):
        """유저의 요청을 DB에 저장"""
        add_support(str(ctx.author.id), message)
        await ctx.send(f"✅ {ctx.author.mention}, 요청이 접수되었습니다!")

async def setup(bot):
    await bot.add_cog(Support(bot))
