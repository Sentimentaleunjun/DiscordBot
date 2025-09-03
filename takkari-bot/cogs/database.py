import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from utils.db import DB_PATH

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dblookup", description="데이터베이스 내용을 확인합니다 (관리자 전용)")
    async def dblookup(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM support_requests")
        support_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM patch_notes")
        patch_count = cur.fetchone()[0]
        conn.close()

        embed = discord.Embed(title="데이터베이스 조회", color=discord.Color.purple())
        embed.add_field(name="문의 개수", value=str(support_count), inline=False)
        embed.add_field(name="패치노트 개수", value=str(patch_count), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Database(bot))
