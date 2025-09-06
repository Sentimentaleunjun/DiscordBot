import discord
from discord import app_commands
from discord.ext import commands

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="db_lookup", description="DB를 조회합니다.")
    async def db_lookup(self, interaction: discord.Interaction, key: str):
        # TODO: db.py에서 불러오기
        await interaction.response.send_message(f"🔍 DB 조회: {key} → 결과 없음")

async def setup(bot):
    await bot.add_cog(DBLookup(bot))

