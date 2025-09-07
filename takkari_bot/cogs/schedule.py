import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot = bot

    @app_commands.command(name="schedule", description="등록된 일정 확인")
    async def schedule(self, interaction: discord.Interaction):
        schedules = db.get_schedules()
        if not schedules:
            await interaction.response.send_message("📅 등록된 일정이 없습니다.", ephemeral=True)
            return
        text = "\n".join([f"- {s[1]}" for s in schedules])
        await interaction.response.send_message(f"📅 일정 목록:\n{text}", ephemeral=True)

    @app_commands.command(name="addschedule", description="일정 추가 (관리자 전용)")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_schedule(self, interaction: discord.Interaction, content: str):
        db.add_schedule(content)
        await interaction.response.send_message(f"✅ 일정 추가됨: {content}", ephemeral=True)

    @app_commands.command(name="removeschedule", description="일정 삭제 (관리자 전용)")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_schedule(self, interaction: discord.Interaction, schedule_id: int):
        db.remove_schedule(schedule_id)
        await interaction.response.send_message(f"🗑️ ID {schedule_id} 일정이 삭제되었습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
