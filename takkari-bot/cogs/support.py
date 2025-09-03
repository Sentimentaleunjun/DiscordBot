import discord, sqlite3
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="support", description="고객지원 문의 등록")
    async def support(self, ctx, *, message: str):
        conn = sqlite3.connect("db/bot.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO tickets (user, message) VALUES (?, ?)", (str(ctx.author), message))
        conn.commit()
        conn.close()
        await ctx.send(f"✅ 문의가 등록되었습니다. 감사합니다, {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(Support(bot))
