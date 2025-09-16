# takkari_bot/cogs/patchnote.py
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import db  # 아까 만든 db.py

# 운영진/제작자 역할 ID
ADMIN_ROLES = [1416769282380922991, 1416769872284876931]
PATCHNOTE_CHANNEL_ID = 1417426181942153237

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # 패치노트 등록
    @app_commands.command(name="add_patchnote", description="운영진/제작자 전용 패치노트 등록")
    @app_commands.describe(title="제목", content="내용")
    async def add_patchnote(self, interaction: discord.Interaction, title: str, content: str):
        # 권한 확인
        if not any(role.id in ADMIN_ROLES for role in interaction.user.roles):
            await interaction.response.send_message("❌ 당신은 패치노트를 등록할 권한이 없습니다.", ephemeral=True)
            return

        # DB에 저장
        db.add_patchnote(title, content, str(interaction.user.id))

        # 채널에 자동 업로드
        channel = self.bot.get_channel(PATCHNOTE_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title=f"📝 {title}",
                description=content,
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text=f"등록자: {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await channel.send(embed=embed)

        await interaction.response.send_message("✅ 패치노트 등록 완료!", ephemeral=True)

    # -----------------------------
    # 패치노트 확인
    @app_commands.command(name="patchnote", description="최근 패치노트 확인")
    async def patchnote(self, interaction: discord.Interaction):
        notes = db.get_patchnotes(5)  # 최근 5개
        if not notes:
            await interaction.response.send_message("❌ 등록된 패치노트가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📜 최근 패치노트",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        for note in notes:
            embed.add_field(
                name=f"{note[1]} ({note[4]})",  # title + created_at
                value=note[2],  # content
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))