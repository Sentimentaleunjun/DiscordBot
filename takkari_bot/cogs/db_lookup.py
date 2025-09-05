import discord
from discord.ext import commands
from takkari_bot.utils.db import get_supports

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dblookup")
    async def dblookup(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("⛔ 관리자만 가능합니다.")
            return
        supports = get_supports()
        if not supports:
            await ctx.send("📭 문의가 없습니다.")
        else:
            msg = "\n".join([f"{u}: {m}" for u, m in supports[:10]])
            await ctx.send(f"📌 최근 문의:\n{msg}")

async def setup(bot):
    await bot.add_cog(DBLookup(bot))
