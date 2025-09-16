import discord
from discord.ext import commands
import sqlite3
import os

PATCH_CHANNEL_ID = 1417426181942153237
ADMIN_ROLE_IDS = [1416769282380922991, 1416769872284876931]
DB_PATH = "db.sqlite"

class PatchNoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, member):
        return any(role.id in ADMIN_ROLE_IDS for role in member.roles)

    @commands.command(name="addpatch")
    async def add_patch(self, ctx, title: str, *, content: str):
        """운영진 전용 패치노트 등록"""
        if not self.is_admin(ctx.author):
            await ctx.send("❌ 이 명령어를 사용할 권한이 없습니다.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patchnotes (title, content, author_id) VALUES (?, ?, ?)",
            (title, content, ctx.author.id)
        )
        conn.commit()
        conn.close()

        embed = discord.Embed(title=title, description=content, color=discord.Color.green())
        await self.bot.get_channel(PATCH_CHANNEL_ID).send(embed=embed)
        await ctx.send("✅ 패치노트 등록 완료!")

    @commands.command(name="patches")
    async def view_patches(self, ctx):
        """모든 유저가 볼 수 있는 패치노트 조회"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, created_at FROM patchnotes ORDER BY created_at DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await ctx.send("등록된 패치노트가 없습니다.")
            return

        embed = discord.Embed(title="최근 패치노트", color=discord.Color.blue())
        for title, content, created_at in rows:
            embed.add_field(name=title, value=f"{content}\n🕒 {created_at}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PatchNoteCog(bot))