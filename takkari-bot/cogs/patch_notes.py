import sqlite3
import discord
from discord.ext import commands
from utils.db import DB_PATH

class PatchNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="patchnotes")
    async def patchnotes_command(self, ctx):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT version, content, created_at FROM patch_notes ORDER BY id DESC LIMIT 5")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            await ctx.send("등록된 패치노트가 없습니다.")
            return

        embed = discord.Embed(title="최근 패치노트", color=discord.Color.green())
        for row in rows:
            embed.add_field(name=f"버전 {row[0]} ({row[2]})", value=row[1], inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchNotes(bot))
