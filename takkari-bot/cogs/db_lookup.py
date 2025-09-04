import discord
from discord.ext import commands
from takkari-bot.utils.db import get_support

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dblookup")
    async def dblookup(self, ctx):
        if ctx.author.id != self.bot.admin_id:
            await ctx.send("⛔ 관리자 전용 명령어입니다.")
            return

        rows = get_support()
        if not rows:
            await ctx.send("📭 문의 내역이 없습니다.")
        else:
            msg = "\n".join([f"[{d}] {u}: {c}" for u, c, d in rows[:5]])
            await ctx.send(f"📑 최근 문의 내역:\n{msg}")

async def setup(bot):
    await bot.add_cog(dblookup(bot))
