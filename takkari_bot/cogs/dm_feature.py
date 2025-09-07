import discord
from discord.ext import commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm")
    async def send_dm(self, ctx, user: discord.User, *, message: str):
        try:
            await user.send(f"📨 {ctx.author} : {message}")
            await ctx.send(f"✅ {user}님에게 DM을 보냈습니다.")
        except discord.Forbidden:
            await ctx.send("❌ DM을 보낼 수 없습니다 (차단 또는 닫힘).")

async def setup(bot):
    await bot.add_cog(DMFeature(bot))
