import discord
from discord.ext import commands
from takkari_bot.utils.db import add_support

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="support")
    async def support(self, ctx, *, content: str):
        add_support(str(ctx.author.id), content)
        await ctx.send("?벃 臾몄쓽媛 ?묒닔?섏뿀?듬땲?? 愿由ъ옄媛 ?뺤씤 ???듬??쒕━寃좎뒿?덈떎.")

async def setup(bot):
    await bot.add_cog(Support(bot))
