import discord
from discord.ext import commands
from takkari-bot.utils.db import add_support

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="support")
    async def support(self, ctx, *, content: str):
        add_support(str(ctx.author.id), content)
        await ctx.send("📩 문의가 접수되었습니다. 관리자가 확인 후 답변드리겠습니다.")

async def setup(bot):
    await bot.add_cog(Support(bot))
