import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from takkari_bot.utils import db

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db.init_points_table()
        db.init_quiz_table()
        self.attendance = {}  # {user_id: last_attendance_date}

    # 포인트 확인
    @app_commands.command(name="points", description="내 포인트를 확인합니다")
    async def points(self, interaction: discord.Interaction):
        point = db.get_point(interaction.user.id)
        await interaction.response.send_message(f"💎 {interaction.user.mention}님, 현재 포인트: {point}", ephemeral=True)

    # 출석 체크
    @app_commands.command(name="attendance", description="오늘 출석 체크하고 포인트 받기")
    async def attendance(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        today = datetime.utcnow().date()

        last_date = self.attendance.get(user_id)
        if last_date == today:
            await interaction.response.send_message("⚠️ 이미 오늘 출석하셨습니다!", ephemeral=True)
            return

        self.attendance[user_id] = today
        db.add_point(user_id, 10)

        point = db.get_point(user_id)
        role = discord.utils.get(interaction.guild.roles, name="VIP")
        if point >= 100 and role and role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"🎉 출석 완료! 포인트 10 획득 + VIP 뱃지 부여!", ephemeral=True)
        else:
            await interaction.response.send_message(f"🎉 출석 완료! 포인트 10 획득", ephemeral=True)

    # 퀴즈
    @app_commands.command(name="quiz", description="퀴즈를 풀어보세요!")
    async def quiz(self, interaction: discord.Interaction):
        q = db.get_random_quiz()
        if not q:
            await interaction.response.send_message("퀴즈가 아직 준비되지 않았습니다.", ephemeral=True)
            return

        question = q[1]
        await interaction.response.send_message(f"📝 퀴즈: {question}\n정답은 DM으로 알려주세요!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        # 샘플 아재개그 퀴즈 등록
        jokes = [
            ("왜 바다가 짠지 아세요?", "소금 때문에"),
            ("컴퓨터가 배고프면 뭐가 될까요?", "램(ram)이 고파서"),
            ("왜 수학책이 우울할까요?", "문제가 많아서")
        ]
        for q, a in jokes:
            db.add_quiz(q, a)

async def setup(bot):
    await bot.add_cog(FunCog(bot))