import sqlite3
import discord
from discord.ext import commands
from utils.db import DB_PATH

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dblookup")
    @commands.has_permissions(administrator=True)
    async def dblookup_command(self, ctx, table: str):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT * FROM {table} LIMIT 10")
            rows = cur.fetchall()
            if not rows:
                await ctx.send("데이터가 없습니다.")
                return
            result = "\n".join([str(r) for r in rows])
            await ctx.send(f"```{result}```")
        except sqlite3.Error:
            await ctx.send("잘못된 테이블 이름입니다.")
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(DBLookup(bot))
