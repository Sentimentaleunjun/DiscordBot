# takkari_bot/cogs/dm_feature.py
import discord
from discord.ext import commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

     @app_commands.command(name="dm", description="서버의 어느 사람에게 Dm를 보냅니다 💘")
    async def send_dm(self, ctx, user: discord.User, *, message: str):
        try:
            sender_tag = f"{ctx.author.name}#{ctx.author.discriminator}"
            await user.send(f"📨 {sender_tag} 님이 보낸 메시지:\n{message}")
            await ctx.send(f"✅ {user}님에게 DM을 전송했습니다.")
        except discord.Forbidden:
            await ctx.send("❌ DM을 보낼 수 없습니다 (차단 or 닫힘).")

async def setup(bot):
    await bot.add_cog(DMFeature(bot))
