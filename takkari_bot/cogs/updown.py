import discord
from discord.ext import commands
from discord import app_commands
import random

# 사용자별 게임 상태 저장
user_games = {}

class UpDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="updown_start", description="업다운 게임 시작 📌 (1~100 숫자 맞추기)")
    async def start_game(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in user_games:
            await interaction.response.send_message("TKR 002 오류. 이미 게임중 입니다.", ephemeral=True)
            return

        number = random.randint(1, 100)
        user_games[user_id] = number
        await interaction.response.send_message("🎮 업다운 게임 시작! 1~100 사이 숫자를 맞춰보세요. `/updown_guess <숫자>`", ephemeral=True)

    @app_commands.command(name="updown_guess", description="숫자를 추측합니다 💥")
    @app_commands.describe(guess="1~100 사이 숫자를 입력하세요")
    async def guess_number(self, interaction: discord.Interaction, guess: int):
        user_id = interaction.user.id
        if user_id not in user_games:
            await interaction.response.send_message("TKR 003 오류 , 먼저 `/updown_start`로 게임을 시작하세요.", ephemeral=True)
            return

        target = user_games[user_id]
        if guess < target:
            await interaction.response.send_message("⬆️ UP! 더 큰 숫자입니다.", ephemeral=True)
        elif guess > target:
            await interaction.response.send_message("⬇️ DOWN! 더 작은 숫자입니다.", ephemeral=True)
        else:
            await interaction.response.send_message(f"🎉 정답! {target} 맞췄습니다!", ephemeral=True)
            del user_games[user_id]

async def setup(bot: commands.Bot):
    await bot.add_cog(UpDown(bot))
