# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="도움말")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="따까리봇 도움말",
            description="사용 가능한 명령어입니다.",
            color=0x00ffcc
        )
        embed.add_field(name="!지원 <메시지>", value="지원 메시지 남기기", inline=False)
        embed.add_field(name="!예약공지 <초> <메시지>", value="예약 공지 등록", inline=False)
        embed.add_field(name="!패치노트", value="최근 패치노트 확인", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
