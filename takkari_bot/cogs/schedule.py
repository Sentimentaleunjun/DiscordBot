import discord
from discord.ext import commands
from discord import app_commands

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedules = {}  # {guild_id: [일정들]}

    @app_commands.command(
        name="addschedule",
        description="서버 전체 일정 등록 (관리자 전용, 드롭다운 UI)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def addschedule(self, interaction: discord.Interaction, *, content: str):
        guild_id = interaction.guild.id
        self.schedules.setdefault(guild_id, []).append(content)

        # 등록 후 기존 일정과 합쳐서 선택 가능하게 드롭다운 생성
        schedules = self.schedules[guild_id]

        class ScheduleView(discord.ui.View):
            def __init__(self, schedules):
                super().__init__(timeout=60.0)
                options = [
                    discord.SelectOption(label=f"{idx+1}. {s}", value=str(idx))
                    for idx, s in enumerate(schedules)
                ]
                self.add_item(RemoveSelect(options, schedules))

        class RemoveSelect(discord.ui.Select):
            def __init__(self, options, schedules):
                super().__init__(placeholder="삭제할 일정 선택", min_values=1, max_values=1, options=options)
                self.schedules = schedules

            async def callback(self, select_interaction: discord.Interaction):
                idx = int(self.values[0])
                removed = self.schedules.pop(idx)
                await select_interaction.response.send_message(f"🗑️ 일정 삭제됨: {removed}", ephemeral=True)
                self.view.stop()

        await interaction.response.send_message(
            f"✅ 일정 등록됨: {content}\n아래에서 기존 일정 삭제 가능:",
            view=ScheduleView(schedules),
            ephemeral=True
        )

    @app_commands.command(
        name="schedule",
        description="등록된 일정을 확인합니다."
    )
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

    @app_commands.command(
        name="removeschedule",
        description="일정을 삭제합니다. (드롭다운 선택, 관리자 전용)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def removeschedule(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        schedules = self.schedules.get(guild_id, [])

        if not schedules:
            await interaction.response.send_message("📭 삭제할 일정이 없습니다.", ephemeral=True)
            return

        class RemoveView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60.0)
                options = [
                    discord.SelectOption(label=f"{idx+1}. {s}", value=str(idx))
                    for idx, s in enumerate(schedules)
                ]
                self.add_item(RemoveSelect(options, schedules))

        class RemoveSelect(discord.ui.Select):
            def __init__(self, options, schedules):
                super().__init__(placeholder="삭제할 일정 선택", min_values=1, max_values=1, options=options)
                self.schedules = schedules

            async def callback(self, select_interaction: discord.Interaction):
                idx = int(self.values[0])
                removed = self.schedules.pop(idx)
                await select_interaction.response.send_message(f"🗑️ 일정 삭제됨: {removed}", ephemeral=True)
                self.view.stop()

        await interaction.response.send_message("삭제할 일정을 선택하세요:", view=RemoveView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
