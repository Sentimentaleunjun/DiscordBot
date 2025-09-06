import discord
from discord.ext import commands

class AccordingToBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="accordingtobot")
    async def accordingtobot(self, ctx, *, content: str):
        if ctx.author.id != self.bot.admin_id:
            await ctx.send("??愿由ъ옄留?媛?ν빀?덈떎.")
            return
        await ctx.send(f"?뱼 怨듭?: {content}")

async def setup(bot):
    await bot.add_cog(AccordingToBot(bot))
