import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db

DEVELOPER_ID = 909360134566862878

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db.init_support_table()

    @app_commands.command(name="support", description="문의/피드백 등록")
    async def support(self, interaction: discord.Interaction, message: str):
        try:
            db.add_support(str(interaction.user.id), message)
            await interaction.response.send_message("✅ 문의가 등록되었습니다!", ephemeral=True)
            # DM으로 개발자에게 전달
            dev = await self.bot.fetch_user(DEVELOPER_ID)
            await dev.send(f"📩 문의 등록됨\n{interaction.user} : {message}")
        except Exception as e:
            await interaction.response.send_message(f"⚠️ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(name="supportlist", description="등록된 문의 목록 확인 (개발자 전용)")
    async def supportlist(self, interaction: discord.Interaction):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 개발자 전용 명령어입니다.", ephemeral=True)
            return
        rows = db.get_supports()
        if not rows:
            await interaction.response.send_message("📭 등록된 문의가 없습니다.", ephemeral=True)
            return
        embed = discord.Embed(title="📋 문의 목록", color=discord.Color.green())
        for r in rows:
            status = "🟢 열림" if r[3]=="open" else "🔴 닫힘"
            user = await self.bot.fetch_user(int(r[1]))
            embed.add_field(
                name=f"ID {r[0]} - {user} [{status}]",
                value=f"{r[2]} ({r[4]})",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="supportclose", description="문의 닫기 (개발자 전용)")
    async def supportclose(self, interaction: discord.Interaction, support_id: int):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ 개발자 전용 명령어입니다.", ephemeral=True)
            return
        rows = db.execute("SELECT user_id FROM support WHERE id=?", (support_id,), fetch=True)
        if not rows:
            await interaction.response.send_message("❌ 해당 문의를 찾을 수 없습니다.", ephemeral=True)
            return
        success = db.close_support(support_id)
        if success:
            user = await self.bot.fetch_user(int(rows[0][0]))
            await user.send(f"✅ 당신의 문의(ID:{support_id})가 해결되었습니다.")
            await interaction.response.send_message(f"✅ 문의 {support_id} 닫힘", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ 문의 {support_id} 이미 닫혀있음", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Support(bot))
