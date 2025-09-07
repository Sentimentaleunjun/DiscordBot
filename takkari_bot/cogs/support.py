import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

DEVELOPER_ID = 909360134566862878

class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 문의 등록
    @app_commands.command(name="support", description="따까리봇 개발자에게 문의/피드백을 보냅니다.")
    async def support(self, interaction: discord.Interaction, message: str):
        try:
            await interaction.response.defer(ephemeral=True)  # ✅ 타임아웃 방지

            # DB에 문의 저장
            db.add_support(str(interaction.user.id), message)

            # 개발자 DM
            dev = await self.bot.fetch_user(DEVELOPER_ID)
            await dev.send(f"📩 {interaction.user} 가 보낸 메시지 : {message}")

            await interaction.followup.send("✅ 문의가 등록되었습니다!", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"⚠️ 오류 발생: {e}", ephemeral=True)

    # 문의 목록 확인 (개발자 전용)
    @app_commands.command(name="supportlist", description="등록된 문의 목록을 확인 (개발자 전용)")
    async def supportlist(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if interaction.user.id != DEVELOPER_ID:
            await interaction.followup.send("❌ 이 명령어는 개발자 전용입니다.", ephemeral=True)
            return

        rows = db.get_supports()
        if not rows:
            await interaction.followup.send("📭 아직 등록된 문의가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(title="📋 따까리봇 문의 리스트", color=discord.Color.green())
        for r in rows:
            status = "🟢 열림" if r[3] == "open" else "🔴 닫힘"
            embed.add_field(
                name=f"ID {r[0]} - User {r[1]} [{status}]",
                value=f"{r[2]} ({r[4]})",
                inline=False
            )

        await interaction.followup.send(embed=embed, ephemeral=True)

    # 문의 닫기 (개발자 전용)
    @app_commands.command(name="supportclose", description="특정 문의를 닫습니다 (개발자 전용)")
    async def supportclose(self, interaction: discord.Interaction, support_id: int):
        await interaction.response.defer(ephemeral=True)

        if interaction.user.id != DEVELOPER_ID:
            await interaction.followup.send("❌ 이 명령어는 개발자 전용입니다.", ephemeral=True)
            return

        try:
            # DB에서 문의 닫기 (성공 여부 + user_id 리턴하도록 수정 필요)
            success, user_id = db.close_support(support_id)

            if success:
                await interaction.followup.send(f"✅ ID {support_id} 문의가 닫혔습니다.", ephemeral=True)

                # 문의 등록자에게 DM 발송
                user = await self.bot.fetch_user(int(user_id))
                await user.send(f"📪 당신의 문의(ID {support_id})가 처리되어 닫혔습니다. 감사합니다!")

            else:
                await interaction.followup.send(f"⚠️ ID {support_id} 문의를 찾을 수 없습니다.", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"⚠️ 오류 발생: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Support(bot))
