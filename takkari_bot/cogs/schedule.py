# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio

class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="예약공지")
    async def schedule(self, ctx, seconds: int, *, message: str):
        """seconds초 후 예약 공지"""
        await ctx.send(f"⏰ {seconds}초 후 공지가 발송됩니다!")
        await asyncio.sleep(seconds)
        embed = discord.Embed(title="📢 예약 공지", description=message, color=0x33ccff)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ScheduleCog(bot))
