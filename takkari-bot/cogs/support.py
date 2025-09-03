import sqlite3
import discord
from discord.ext import commands
from utils.db import DB_PATH

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="support")
    async def support_command(self, ctx, *, message: str):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO support_requests (user_id, message) VALUES (?, ?)", (str(ctx.author.id), message))
        conn.commit()
        conn.close()
        await ctx.send("문의가 정상적으로 접수되었습니다!")

async def setup(bot):
    await bot.add_cog(Support(bot))
