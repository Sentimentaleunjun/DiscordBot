import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo_command(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name} 서버 정보", color=discord.Color.gold())
        embed.add_field(name="서버 ID", value=guild.id, inline=False)
        embed.add_field(name="멤버 수", value=guild.member_count, inline=False)
        embed.add_field(name="소유자", value=guild.owner, inline=False)
        embed.add_field(name="생성일", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
