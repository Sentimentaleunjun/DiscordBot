import discord
from discord.ext import commands
from takkari_bot.utils.db import get_supports

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dblookup")
    async def dblookup(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("??愿由ъ옄留?媛?ν빀?덈떎.")
            return
        supports = get_supports()
        if not supports:
            await ctx.send("?벊 臾몄쓽媛 ?놁뒿?덈떎.")
        else:
            msg = "\n".join([f"{u}: {m}" for u, m in supports[:10]])
            await ctx.send(f"?뱦 理쒓렐 臾몄쓽:\n{msg}")

async def setup(bot):
    await bot.add_cog(DBLookup(bot))
