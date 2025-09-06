import discord
from discord.ext import commands
from discord import app_commands

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedules = []  # 메모리 저장 (DB 연결 가능)

    @app_commands.command(name="schedule", description="일정을 확인합니다.")
    async def schedule(self, interaction: discord.Interaction):
        if not self.schedules:
            await interaction.response.send_message("📅 등록된 일정이 없습니다.", ephemeral=True)
        else:
            text = "\n".join([f"- {s}" for s in self.schedules])
            await interaction.response.send_message(f"📅 일정 목록:\n{text}", ephemeral=True)

    @app_commands.command(name="addschedule", description="일정을 추가합니다.")
    async def add_schedule(self, interaction: discord.Interaction, content: str):
        self.schedules.append(content)
        await interaction.response.send_message(f"✅ 일정 추가됨: {content}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
