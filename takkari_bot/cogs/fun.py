import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from takkari_bot.utils import db

# 뱃지 역할 이름
ATTENDANCE_ROLE_NAME = "출석왕 🎖️"
QUIZ_ROLE_NAME = "아재개그 달인 🏆"

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attendance_check.start()
        db.init_db()

        # 아재개그 퀴즈 초기 등록 (DB에 중복 없이)
        sample_quizzes = [
            ("왜 컴퓨터는 바다를 싫어할까요?", "너무 많은 '버그'가 있어서요!🤣"),
            ("왜 수학책은 슬펐을까요?", "문제가 많아서요😂"),
            ("왜 고양이는 컴퓨터를 좋아할까요?", "마우스를 좋아해서🐱💻")
        ]
        for q, a in sample_quizzes:
            db.add_quiz(q, a)

    # ----------------- 출석 체크 -----------------
    @tasks.loop(hours=24)
    async def attendance_check(self):
        for guild in self.bot.guilds:
            role = discord.utils.get(guild.roles, name=ATTENDANCE_ROLE_NAME)
            if role is None:
                role = await guild.create_role(name=ATTENDANCE_ROLE_NAME, colour=discord.Colour.gold())

            for member in guild.members:
                if member.bot:
                    continue
                if role not in member.roles:
                    await member.add_roles(role)

    @attendance_check.before_loop
    async def before_attendance(self):
        await self.bot.wait_until_ready()

    # ----------------- 퀴즈 -----------------
    @app_commands.command(name="quiz", description="랜덤 아재개그 퀴즈를 풀어보세요!")
    async def quiz(self, interaction: discord.Interaction):
        quiz_data = db.get_random_quiz()
        if not quiz_data:
            await interaction.response.send_message("퀴즈가 없습니다! 😢", ephemeral=True)
            return
        q_id, question, answer = quiz_data
        await interaction.response.send_message(f"문제: {question}\n정답은 `{answer}`", ephemeral=True)

        # 퀴즈 완료 시 뱃지 역할 부여
        role = discord.utils.get(interaction.guild.roles, name=QUIZ_ROLE_NAME)
        if role is None:
            role = await interaction.guild.create_role(name=QUIZ_ROLE_NAME, colour=discord.Colour.green())
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.followup.send(f"축하합니다! '{QUIZ_ROLE_NAME}' 역할이 부여되었습니다 🏆", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCog(bot))