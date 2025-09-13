import discord
from discord import app_commands
from discord.ext import commands

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="공지 메시지를 전송합니다. (관리자만 사용 가능)")
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, *, message: str):
        embed = discord.Embed(title="📢 공지", description=message, color=discord.Color.gold())
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ {channel.mention} 에 공지가 전송되었습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announce(bot))
