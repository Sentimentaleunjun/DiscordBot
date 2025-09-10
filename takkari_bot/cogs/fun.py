# takkari_bot/cogs/fun.py
import discord
from discord import app_commands
from discord.ext import commands
from takkari_bot.utils import db, logging_config
import random

logger = logging_config.setup_logging()

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db.init_db()  # Cog 로드 시 DB 초기화
        logger.info("FunCog loaded and DB initialized.")

    # 가위바위보
    @app_commands.command(name="rps", description="가위바위보 게임을 합니다.")
    @app_commands.describe(choice="가위, 바위, 보 중 하나를 선택하세요.")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ["가위", "바위", "보"]
        choice = choice.strip()
        if choice not in choices:
            await interaction.response.send_message("❌ 가위, 바위, 보 중에서 선택해주세요!", ephemeral=True)
            logger.warning(f"{interaction.user} tried invalid RPS choice: {choice}")
            return

        bot_choice = random.choice(choices)
        result = ""
        if choice == bot_choice:
            result = "무승부! 🤝"
        elif (choice == "가위" and bot_choice == "보") or \
             (choice == "바위" and bot_choice == "가위") or \
             (choice == "보" and bot_choice == "바위"):
            result = "승리! 🎉"
            db.add_point(interaction.user.id, 10)
            logger.info(f"{interaction.user} won RPS, 10 points added.")
        else:
            result = "패배 😢"
            logger.info(f"{interaction.user} lost RPS.")

        await interaction.response.send_message(
            f"너: {choice}\n봇: {bot_choice}\n결과: {result}\n💰 현재 포인트: {db.get_point(interaction.user.id)}점",
            ephemeral=True
        )

    # 포인트 확인
    @app_commands.command(name="points", description="내 포인트를 확인합니다.")
    async def points(self, interaction: discord.Interaction):
        user_points = db.get_point(interaction.user.id)
        await interaction.response.send_message(f"💰 {interaction.user.name}님의 포인트: {user_points}점", ephemeral=True)
        logger.info(f"{interaction.user} checked points: {user_points}")

    # 퀴즈
    @app_commands.command(name="quiz", description="퀴즈를 출제하고 풀어보세요!")
    async def quiz(self, interaction: discord.Interaction):
        quiz = db.get_random_quiz()
        if not quiz:
            await interaction.response.send_message("❌ 등록된 퀴즈가 없습니다!", ephemeral=True)
            logger.warning(f"{interaction.user} tried to get a quiz but none exist.")
            return

        quiz_id, question, answer = quiz
        embed = discord.Embed(title="📝 퀴즈", description=question, color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} received quiz ID {quiz_id}")

async def setup(bot):
    await bot.add_cog(FunCog(bot))