# takkari_bot/cogs/fun.py
import discord
from discord import app_commands
from discord.ext import commands
import random
from . import db  # db.py 불러오기

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tree = app_commands.CommandTree(commands.Bot(command_prefix="/"))

    @app_commands.command(name="rps", description="가위바위보 게임을 합니다!")
    async def rps(self, interaction: discord.Interaction, choice: str):
        # 입력 검사
        if choice.lower() not in ["가위", "바위", "보"]:
            await interaction.response.send_message(
                "❌ 가위/바위/보 중 하나를 선택해주세요!", ephemeral=True
            )
            return

        # defer: interaction 응답 지연 처리
        await interaction.response.defer(ephemeral=True)

        bot_choice = random.choice(["가위", "바위", "보"])
        if choice == bot_choice:
            result = "무승부 🤝"
        elif (
            (choice == "가위" and bot_choice == "보") or
            (choice == "바위" and bot_choice == "가위") or
            (choice == "보" and bot_choice == "바위")
        ):
            result = "승리 🎉"
            db.add_point(interaction.user.id, 10)
        else:
            result = "패배 😢"
            db.add_point(interaction.user.id, 1)

        # followup 사용
        await interaction.followup.send(
            f"너: {choice} | 봇: {bot_choice}\n결과: {result}\n🎯 포인트: {db.get_point(interaction.user.id)}"
        )

    @app_commands.command(name="points", description="자신의 포인트를 확인합니다!")
    async def points(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        pts = db.get_point(interaction.user.id)
        await interaction.followup.send(f"🎯 {interaction.user}님의 포인트: {pts}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Fun(bot))
