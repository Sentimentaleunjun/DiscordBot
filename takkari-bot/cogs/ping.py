import discord
from discord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send(f"핑: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
