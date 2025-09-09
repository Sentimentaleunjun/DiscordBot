import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="schedule", description="일정을 확인합니다.")
    async def schedule(self, interaction: discord.Interaction):
        rows = db.execute("SELECT content FROM schedule ORDER BY rowid DESC", fetch=True)
        if not rows:
            await interaction.response.send_message("📅 등록된 일정이 없습니다.", ephemeral=True)
        else:
            text = "\n".join([f"- {r[0]}" for r in rows])
            await interaction.response.send_message(f"📅 일정 목록:\n{text}", ephemeral=True)

    @app_commands.command(name="addschedule", description="일정을 추가합니다.")
    async def add_schedule(self, interaction: discord.Interaction, content: str):
        db.execute("INSERT INTO schedule (content) VALUES (?)", (content,), commit=True)
        await interaction.response.send_message(f"✅ 일정 추가됨: {content}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))