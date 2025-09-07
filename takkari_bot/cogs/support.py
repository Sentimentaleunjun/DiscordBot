import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

DEVELOPER_ID = 909360134566862878

class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="support",
        description="따까리봇 개발자에게 문의/피드백을 보냅니다."
    )
    async def support(self, interaction: discord.Interaction, message: str):
        try:
            # DB에 문의 저장
            db.add_support(str(interaction.user.id), message)

            # 개발자(너) DM 알림
            dev = await self.bot.fetch_user(DEVELOPER_ID)
            await dev.send(f"📩 {interaction.user} 가 보낸 메시지 : {message}")

            await interaction.response.send_message("✅ 문의가 등록되었습니다!", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"⚠️ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(
        name="supportclose",
        description="특정 문의를 닫습니다 (개발자 전용)"
    )
    async def supportclose(self, interaction: discord.Interaction, support_id: int):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 이 명령어는 개발자 전용입니다.", ephemeral=True)
            return

        try:
            # DB에서 문의 닫기
            success, user_id = db.close_support(support_id)  # 👉 user_id를 반환하도록 db 수정 필요
            if success:
                await interaction.response.send_message(f"✅ ID {support_id} 문의가 닫혔습니다.", ephemeral=True)

                # 문의한 유저에게 DM 알림
                user = await self.bot.fetch_user(int(user_id))
                await user.send(f"📪 당신의 문의(ID {support_id})가 처리되어 닫혔습니다. 감사합니다!")
            else:
                await interaction.response.send_message(f"⚠️ ID {support_id} 문의를 찾을 수 없습니다.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"⚠️ 오류 발생: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Support(bot))
