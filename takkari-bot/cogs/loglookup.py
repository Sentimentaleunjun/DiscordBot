import discord
from discord.ext import commands

class LogLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="loglookup")
    @commands.has_permissions(administrator=True)
    async def loglookup_command(self, ctx):
        try:
            with open("bot.log", "r", encoding="utf-8") as f:
                logs = f.read()[-1800:]  # 마지막 부분만 전송
            await ctx.send(f"```{logs}```")
        except FileNotFoundError:
            await ctx.send("로그 파일이 없습니다.")

async def setup(bot):
    await bot.add_cog(LogLookup(bot))
