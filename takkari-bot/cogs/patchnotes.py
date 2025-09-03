import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from utils.db import DB_PATH

class PatchNotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="patchnotes", description="패치노트를 등록하거나 확인합니다")
    async def patchnotes(self, interaction: discord.Interaction, version: str = None, content: str = None):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        if version and content:
            cur.execute("INSERT INTO patch_notes (version, content) VALUES (?, ?)", (version, content))
            conn.commit()
            await interaction.response.send_message(f"✅ 패치노트 {version}이 등록되었습니다.")
        else:
            cur.execute("SELECT version, content, created_at FROM patch_notes ORDER BY created_at DESC LIMIT 5")
            rows = cur.fetchall()
            if not rows:
                await interaction.response.send_message("등록된 패치노트가 없습니다.")
            else:
                embed = discord.Embed(title="최근 패치노트", color=discord.Color.orange())
                for row in rows:
                    embed.add_field(name=row[0], value=row[1], inline=False)
                await interaction.response.send_message(embed=embed)
        conn.close()

async def setup(bot):
    await bot.add_cog(PatchNotes(bot))
