import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="?뱰 ?꾩?留?, description="?ъ슜 媛?ν븳 紐낅졊??紐⑸줉?낅땲??", color=0x00ffcc)
        embed.add_field(name="/help", value="?꾩?留??뺤씤", inline=False)
        embed.add_field(name="/patchnote", value="?⑥튂?명듃 ?뺤씤/異붽? (愿由ъ옄留?異붽? 媛??", inline=False)
        embed.add_field(name="/support [?댁슜]", value="怨좉컼吏??臾몄쓽 ?깅줉", inline=False)
        embed.add_field(name="/dblookup", value="DB 議고쉶 (愿由ъ옄 ?꾩슜)", inline=False)
        embed.add_field(name="/accordingtobot [?댁슜]", value="怨듭? 諛쒖넚 (愿由ъ옄 ?꾩슜)", inline=False)
        embed.add_field(name="/schedule [YYYY-MM-DD HH:MM] [?댁슜]", value="怨듭? ?덉빟 (愿由ъ옄 ?꾩슜)", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
