import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from utils.db import DB_PATH

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="support", description="따까리봇에 대한 문의를 남깁니다")
    async def support(self, interaction: discord.Interaction, message: str):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO support_requests (user_id, message) VALUES (?, ?)", (str(interaction.user.id), message))
        conn.commit()
        conn.close()
        await interaction.response.send_message("문의가 정상적으로 접수되었습니다. 감사합니다!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))

async def setup(bot):
    await bot.add_cog(HelpCog(bot))


