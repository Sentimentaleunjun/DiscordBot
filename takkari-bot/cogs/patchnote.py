import discord
from discord.ext import commands
from takkari-bot.utils.db import add_patchnote, get_patchnotes

class Patchnote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="patchnote")
    async def patchnote(self, ctx, *, content: str = None):
        if content:
            if ctx.author.id != self.bot.admin_id:
                await ctx.send("⛔ 권한이 없습니다.")
                return
            add_patchnote(content)
            await ctx.send("✅ 패치노트가 등록되었습니다.")
        else:
            notes = get_patchnotes()
            if not notes:
                await ctx.send("📭 등록된 패치노트가 없습니다.")
            else:
                msg = "\n".join([f"- {c} ({d})" for c, d in notes])
                await ctx.send(f"📌 최신 패치노트:\n{msg}")

async def setup(bot):
    await bot.add_cog(Patchnote(bot))
