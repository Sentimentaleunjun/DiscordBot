# db_lookup.py
import discord
from discord import app_commands
from discord.ext import commands

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
     def cog_load(self):
        self.bot.tree.add_command(self.dblookup)

    @app_commands.command(name="dblookup", description="DB를 조회합니다.")
    async def db_lookup(self, interaction: discord.Interaction, key: str):
        # TODO: 실제 DB 연동
        await interaction.response.send_message(f"🔍 DB 조회: `{key}` → 결과 없음", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DBLookup(bot))
