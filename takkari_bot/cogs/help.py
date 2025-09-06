# cogs/help.py
import discord
from discord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def show_help(self, ctx):
        """따까리봇 소개 & 명령어 안내"""
        embed = discord.Embed(
            title="🤖 따까리봇 사용 가이드",
            description="서버 관리와 편의 기능을 제공하는 **GSEJ Company** 제작 봇입니다.",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="📅 스케줄",
            value="`!addschedule` (관리자) → 서버 전체 일정 등록\n"
                  "`!schedule` → 일정 확인",
            inline=False
        )
        embed.add_field(
            name="🔍 데이터 조회",
            value="`!dblookup` (관리자)\n`!loglookup` (관리자)",
            inline=False
        )
        embed.add_field(
            name="📨 고객 지원",
            value="`/support` → 문의 등록\n`/supportlist` (개발자만)",
            inline=False
        )
        embed.add_field(
            name="⚙️ 기타",
            value="`!userinfo @유저`\n`!dm @유저 <메시지>` (관리자)",
            inline=False
        )

        embed.add_field(
            name="🌐 개발사",
            value="[GSEJ Company](https://gsej-company.onrender.com)",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
