import discord
from discord.ext import commands
from takkari_bot.utils.db import add_patchnote, get_patchnotes

class Patchnote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="patchnote")
    async def patchnote(self, ctx, *, content: str = None):
        if content:
            if ctx.author.id != self.bot.admin_id:
                await ctx.send("??沅뚰븳???놁뒿?덈떎.")
                return
            add_patchnote(content)
            await ctx.send("???⑥튂?명듃媛 ?깅줉?섏뿀?듬땲??")
        else:
            notes = get_patchnotes()
            if not notes:
                await ctx.send("?벊 ?깅줉???⑥튂?명듃媛 ?놁뒿?덈떎.")
            else:
                msg = "\n".join([f"- {c} ({d})" for c, d in notes])
                await ctx.send(f"?뱦 理쒖떊 ?⑥튂?명듃:\n{msg}")

async def setup(bot):
    await bot.add_cog(Patchnote(bot))
