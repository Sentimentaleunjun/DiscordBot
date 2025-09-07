import discord
from discord.ext import commands
from discord import app_commands

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedules = {}  # {guild_id: [일정들]} 저장 예시

    @app_commands.command(name="addschedule", description="서버 전체 일정 등록 (관리자 전용)")
    @app_commands.checks.has_permissions(administrator=True)
    async def addschedule(self, interaction: discord.Interaction, *, content: str):
        guild_id = interaction.guild.id
        self.schedules.setdefault(guild_id, []).append(content)
        await interaction.response.send_message(f"✅ 일정 등록됨: {content}", ephemeral=True)

    @app_commands.command(name="schedule", description="등록된 일정을 확인합니다.")
    async def schedule(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        schedules = self.schedules.get(guild_id, [])
        if not schedules:
            await interaction.response.send_message("📭 등록된 일정이 없습니다.", ephemeral=True)
        else:
            embed = discord.Embed(title="📅 서버 일정", color=discord.Color.green())
            for idx, item in enumerate(schedules, 1):
                embed.add_field(name=f"{idx}.", value=item, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="removeschedule", description="일정을 삭제합니다. (관리자 전용)")
    @app_commands.checks.has_permissions(administrator=True)
    async def removeschedule(self, interaction: discord.Interaction, index: int):
        guild_id = interaction.guild.id
        schedules = self.schedules.get(guild_id, [])

        if 0 < index <= len(schedules):
            removed = schedules.pop(index - 1)
            await interaction.response.send_message(f"🗑️ 일정 삭제됨: {removed}", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ 잘못된 번호입니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
