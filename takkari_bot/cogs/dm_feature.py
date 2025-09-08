# takkari_bot/cogs/dm_feature.py
import discord
from discord.ext import commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm")
    async def send_dm(self, ctx, user: discord.User, *, message: str):
        """모든 유저가 사용 가능, 보낸 사람 이름 표시"""
        try:
            sender_tag = f"{ctx.author.name}#{ctx.author.discriminator}"
            await user.send(f"📨 {sender_tag} 님이 보낸 메시지:\n{message}")
            await ctx.send(f"✅ {user}님에게 DM을 전송했습니다.")
        except discord.Forbidden:
            await ctx.send("❌ DM을 보낼 수 없습니다 (차단 or 닫힘).")

async def setup(bot):
    await bot.add_cog(DMFeature(bot))
