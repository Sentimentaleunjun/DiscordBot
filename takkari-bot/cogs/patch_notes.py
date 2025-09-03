import discord, sqlite3
from discord.ext import commands

class PatchNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="patchnote", description="패치노트 확인")
    async def patchnote(self, ctx):
        conn = sqlite3.connect("db/bot.db")
        cur = conn.cursor()
        cur.execute("SELECT note FROM patchnotes ORDER BY id DESC LIMIT 5")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            await ctx.send("📜 등록된 패치노트가 없습니다.")
            return
        embed = discord.Embed(title="최근 패치노트", color=discord.Color.blue())
        for r in rows:
            embed.add_field(name="업데이트", value=r[0], inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchNotes(bot))
