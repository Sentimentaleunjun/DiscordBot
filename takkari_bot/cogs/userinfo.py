# userinfo.py
import discord
from discord.ext import commands
from discord import app_commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="유저 정보를 확인합니다.")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        embed = discord.Embed(title="유저 정보", color=discord.Color.blue())
        embed.add_field(name="이름", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="계정 생성일", value=user.created_at.strftime("%Y-%m-%d %H:%M"), inline=False)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
