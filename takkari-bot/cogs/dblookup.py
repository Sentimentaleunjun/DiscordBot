import discord, sqlite3
from discord.ext import commands

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="dblookup", description="서버 관리자가 DB를 조회")
    @commands.has_permissions(administrator=True)
    async def dblookup(self, ctx):
        conn = sqlite3.connect("db/bot.db")
        cur = conn.cursor()
        cur.execute("SELECT id, user, message FROM tickets ORDER BY id DESC LIMIT 5")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            await ctx.send("📂 저장된 문의가 없습니다.")
            return
        embed = discord.Embed(title="최근 문의 목록", color=discord.Color.green())
        for r in rows:
            embed.add_field(name=f"ID {r[0]}", value=f"유저: {r[1]}\n내용: {r[2]}", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DBLookup(bot))
