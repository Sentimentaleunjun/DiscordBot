import discord
from discord.ext import commands
from discord import app_commands
import random
from takkari_bot.utils import db

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot = bot
        db.init_points_table()
        db.init_quiz_table()

    @app_commands.command(name="rps", description="가위바위보 게임")
    async def rps(self, interaction: discord.Interaction, choice: str):
        choice = choice.lower()
        options = ["가위","바위","보"]
        if choice not in options:
            await interaction.response.send_message("❌ 가위/바위/보 중 하나를 선택해주세요!", ephemeral=True)
            return
        bot_choice = random.choice(options)
        result = "무승부"
        if (choice=="가위" and bot_choice=="보") or (choice=="바위" and bot_choice=="가위") or (choice=="보" and bot_choice=="바위"):
            result = "승리"
            db.add_point(interaction.user.id, 10)
        elif choice != bot_choice:
            result = "패배"
            db.add_point(interaction.user.id, 2)
        await interaction.response.send_message(f"너: {choice} | 봇: {bot_choice}\n결과: {result}\n포인트: {db.get_point(interaction.user.id)}")

    @app_commands.command(name="quiz", description="퀴즈 맞추기")
    async def quiz(self, interaction: discord.Interaction):
        quiz = db.get_random_quiz()
        if not quiz:
            await interaction.response.send_message("❌ 퀴즈가 등록되어 있지 않습니다.", ephemeral=True)
            return
        question = quiz[1]
        answer = quiz[2]

        modal = QuizModal(question, answer, interaction.user.id)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="roll", description="주사위 굴리기 (1~6)")
    async def roll(self, interaction: discord.Interaction):
        num = random.randint(1,6)
        db.add_point(interaction.user.id, num)
        await interaction.response.send_message(f"🎲 {interaction.user}님이 {num} 나왔습니다! 포인트 +{num} | 현재 포인트: {db.get_point(interaction.user.id)}")

    @app_commands.command(name="points", description="현재 포인트 확인")
    async def points(self, interaction: discord.Interaction):
        pts = db.get_point(interaction.user.id)
        await interaction.response.send_message(f"🎯 {interaction.user}님의 포인트: {pts}", ephemeral=True)


# ---------------- Modal for Quiz ----------------
from discord.ui import Modal, TextInput

class QuizModal(Modal):
    def __init__(self, question, answer, user_id):
        super().__init__(title="퀴즈 도전!")
        self.answer = answer.lower()
        self.user_id = user_id
        self.add_item(TextInput(label=question, placeholder="정답을 입력하세요"))

    async def on_submit(self, interaction: discord.Interaction):
        user_answer = self.children[0].value.lower()
        if user_answer == self.answer:
            db.add_point(self.user_id, 20)
            await interaction.response.send_message(f"✅ 정답! 포인트 +20 | 현재 포인트: {db.get_point(self.user_id)}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ 오답! 정답: {self.answer} | 포인트: {db.get_point(self.user_id)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
