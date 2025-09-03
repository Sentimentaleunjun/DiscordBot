import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo")
    async def userinfo_command(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name} 유저 정보", color=discord.Color.purple())
        embed.add_field(name="유저 ID", value=member.id, inline=False)
        embed.add_field(name="계정 생성일", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="서버 가입일", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
