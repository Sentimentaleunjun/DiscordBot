# riot.py
import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import request
import urllib.parse
import requests
import sqlite3
from main import DB_PATH, app  # main.py에서 DB_PATH와 Flask 앱 불러오기

class RiotOAuth(commands.Cog):
    """라이엇 OAuth 로그인 + 토큰 발급 + DB 저장 + Discord DM 안내"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Flask 콜백 라우트 등록
        @app.route("/riot/callback")
        def riot_callback():
            code = request.args.get("code")
            state = request.args.get("state")  # Discord 사용자 ID
            if not code or not state:
                return "TKR 002 오류: 로그인 코드 또는 상태값이 없습니다.", 400

            try:
                user_id = int(state)
                user = self.bot.get_user(user_id)
                if not user:
                    return "Discord 유저를 찾을 수 없습니다.", 400

                # 토큰 발급 요청 (예시)
                token_url = "https://auth.riotgames.com/token"
                client_id = os.environ.get("RIOT_CLIENT_ID")
                client_secret = os.environ.get("RIOT_CLIENT_SECRET")
                redirect_uri = os.environ.get("RIOT_REDIRECT_URI")
                data = {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": client_id,
                    "client_secret": client_secret
                }
                r = requests.post(token_url, data=data)
                if r.status_code != 200:
                    return f"토큰 발급 실패: {r.text}", 500

                token_info = r.json()
                access_token = token_info.get("access_token")

                # DB에 저장
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        riot_token TEXT
                    )
                """)
                cursor.execute("""
                    INSERT INTO users(id, riot_token)
                    VALUES(?, ?)
                    ON CONFLICT(id) DO UPDATE SET riot_token=excluded.riot_token
                """, (user_id, access_token))
                conn.commit()
                conn.close()

                # Discord DM 안내
                self.bot.loop.create_task(
                    user.send("✅ 라이엇 로그인 완료! 토큰이 안전하게 저장되었습니다.")
                )

            except Exception as e:
                print(f"[Riot Callback] 오류: {e}")
                return "로그인 처리 중 오류가 발생했습니다.", 500

            return "로그인 완료! Discord DM을 확인하세요."

    @app_commands.command(
        name="login_riot",
        description="라이엇 계정으로 로그인 💘"
    )
    async def login_riot(self, interaction: discord.Interaction):
        client_id = os.environ.get("RIOT_CLIENT_ID")
        redirect_uri = os.environ.get("RIOT_REDIRECT_URI")

        if not client_id or not redirect_uri:
            await interaction.response.send_message(
                "TKR 001 오류: /support로 관리자에게 문의하세요",
                ephemeral=True
            )
            return

        state = str(interaction.user.id)
        oauth_url = (
            "https://auth.riotgames.com/authorize"
            f"?client_id={urllib.parse.quote(client_id)}"
            f"&response_type=code"
            f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
            f"&scope=openid%20account"
            f"&state={urllib.parse.quote(state)}"
        )

        embed = discord.Embed(
            title="라이엇 로그인",
            description="아래 버튼을 눌러 Riot 계정으로 로그인하세요.",
            color=0x1f8b4c
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="로그인", url=oauth_url))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RiotOAuth(bot))