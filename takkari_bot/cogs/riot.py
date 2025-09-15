# riot.py
import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from flask import request, Flask

DB_PATH = "db.sqlite"  # main.py랑 같은 DB 사용

# Flask 앱 가져오기
flask_app = Flask(__name__)

class RiotOAuth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="login_riot", description="라이엇 계정으로 로그인 💘")
    async def login_riot(self, interaction: discord.Interaction):
        client_id = os.environ.get("RIOT_CLIENT_ID")
        redirect_uri = os.environ.get("RIOT_REDIRECT_URI")
        if not client_id or not redirect_uri:
            await interaction.response.send_message("TKR 001 오류 . /support로 관리자에게 문의하세요", ephemeral=True)
            return

        # 로그인 버튼에 discord_id 포함
        oauth_url = (
            f"https://auth.riotgames.com/authorize"
            f"?client_id={client_id}"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}?discord_id={interaction.user.id}"
            f"&scope=openid%20account"
        )

        embed = discord.Embed(
            title="라이엇 로그인",
            description="아래 버튼을 눌러 Riot 계정으로 로그인하세요."
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="로그인", url=oauth_url))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="riot_status", description="라이엇 로그인 상태 확인")
    async def riot_status(self, interaction: discord.Interaction):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM riot_codes WHERE discord_id = ?", (interaction.user.id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            await interaction.response.send_message("✅ 라이엇 로그인 완료", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 로그인 기록 없음", ephemeral=True)


# -----------------------------
# Flask 콜백 엔드포인트
@flask_app.route("/riot/callback")
def riot_callback():
    code = request.args.get("code")
    discord_id = request.args.get("discord_id")

    if not code or not discord_id:
        return "TKR 002 오류. 코드 또는 디스코드 ID가 없습니다."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riot_codes(
        discord_id TEXT PRIMARY KEY,
        code TEXT
    )
    """)
    cursor.execute(
        "REPLACE INTO riot_codes (discord_id, code) VALUES (?, ?)",
        (discord_id, code)
    )
    conn.commit()
    conn.close()

    return "Riot 로그인 성공! 이제 디스코드로 돌아가세요."


async def setup(bot):
    await bot.add_cog(RiotOAuth(bot))