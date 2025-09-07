import discord
from discord.ext import commands
from discord import app_commands

class DMFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dm",
        description="특정 유저에게 DM을 보냅니다."
    )
    async def send_dm(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        message: str
    ):
        """누구나 DM을 보낼 수 있는 기능"""

        try:
            # 보낸 사람 이름/태그
            sender = f"{interaction.user.name}#{interaction.user.discriminator}"

            # DM 내용 (보낸사람 정보 포함)
            content = f"✉️ {sender} 님이 보낸 메시지:\n\n{message}"

            await user.send(content)
            await interaction.response.send_message(
                f"✅ {user.mention} 님에게 DM을 보냈습니다.",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ DM을 보낼 수 없습니다 (상대방이 차단했거나 DM 차단 설정).",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(DMFeature(bot))
