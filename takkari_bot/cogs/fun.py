import discord
from discord.ext import commands, tasks
from discord import app_commands
from takkari_bot.utils import db

BADGE_ROLE_NAME = "따까리봇 출석왕"

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------- 출석 체크 --------------------
    @app_commands.command(name="attendance", description="오늘 출석 체크를 합니다!")
    async def attendance(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=BADGE_ROLE_NAME)

        if role is None:
            role = await guild.create_role(name=BADGE_ROLE_NAME, color=discord.Color.gold())
        
        if role not in member.roles:
            await member.add_roles(role)
            await interaction.response.send_message(f"🎉 {member.display_name}님 출석 완료! 뱃지를 받았습니다!", ephemeral=True)
        else:
            await interaction.response.send_message(f"이미 출석 완료하셨습니다! ✅", ephemeral=True)

    # -------------------- 아재개그 퀴즈 --------------------
    @app_commands.command(name="dadjoke_quiz", description="아재개그 퀴즈를 풀어보세요!")
    async def dadjoke_quiz(self, interaction: discord.Interaction):
        quiz = db.get_random_quiz()
        if not quiz:
            await interaction.response.send_message("퀴즈가 아직 등록되어 있지 않습니다! 😢", ephemeral=True)
            return

        question = quiz[1]
        answer = quiz[2]

        await interaction.response.send_message(f"❓ **퀴즈:** {question}", ephemeral=True)

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if answer.lower() in msg.content.lower():
                await interaction.followup.send(f"✅ 정답! {answer} 맞아요!", ephemeral=True)
            else:
                await interaction.followup.send(f"❌ 틀렸습니다! 정답은 {answer}입니다.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send(f"⏰ 시간 초과! 정답은 {answer}였습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
