# cogs/dm_feature.py
import discord
from discord.ext import commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm")
    @commands.has_permissions(administrator=True)  # 관리자만
    async def send_dm(self, ctx, user: discord.User, *, message: str):
        """특정 유저에게 DM 보내기"""
        try:
            await user.send(message)
            await ctx.send(f"✅ {user} 님에게 DM 보냈습니다.")
        except discord.Forbidden:
            await ctx.send("❌ DM을 보낼 수 없습니다 (차단 or 닫힘).")

async def setup(bot):
    await bot.add_cog(DMFeature(bot))
