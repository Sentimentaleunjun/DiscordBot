import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="서버 정보를 확인합니다")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"서버 정보 - {guild.name}", color=discord.Color.blue())
        embed.add_field(name="서버 ID", value=guild.id, inline=False)
        embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
        embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="유저 정보를 확인합니다")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title=f"유저 정보 - {member}", color=discord.Color.green())
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="가입일", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
        embed.add_field(name="계정 생성일", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
