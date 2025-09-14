# takkari_bot/cogs/dm_feature.py
import discord
from discord.ext import commands
from discord import app_commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dm",
        description="서버의 어느 사람에게 DM을 보냅니다 💌"
    )
    async def send_dm(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        *,
        message: str
    ):
        """슬래시 커맨드로 DM 보내기"""
        try:
            sender_tag = f"{interaction.user.name}#{interaction.user.discriminator}"
            await user.send(f"📨 {sender_tag} 님이 보낸 메시지:\n{message}")
            await interaction.response.send_message(
                f"✅ {user}님에게 DM을 전송했습니다.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ DM을 보낼 수 없습니다 (차단 또는 DM 설정 확인).",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(DMFeature(bot))