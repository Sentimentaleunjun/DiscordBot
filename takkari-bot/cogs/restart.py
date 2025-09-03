import os
import sys
import discord
from discord.ext import commands

DEV_ID = 909360134566862878

class RestartCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    async def restart_command(self, ctx):
        if ctx.author.id != DEV_ID:
            await ctx.send("이 명령어는 개발자만 사용할 수 있습니다.")
            return
        await ctx.send("봇을 재시작합니다...")
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(RestartCommand(bot))
