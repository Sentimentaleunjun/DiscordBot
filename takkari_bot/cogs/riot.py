import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from urllib.parse import urlencode
import os, aiohttp, datetime
from takkari_bot.utils import db

class RiotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- /riotlogin ----------
    @app_commands.command(name="riotlogin", description="Riot 계정으로 로그인")
    async def riotlogin(self, interaction: discord.Interaction):
        client_id = os.environ.get("RIOT_CLIENT_ID")
        redirect_uri = os.environ.get("RIOT_REDIRECT_URI")
        if not client_id or not redirect_uri:
            await interaction.response.send_message("⚠️ Riot OAuth 환경변수가 설정되지 않았습니다.", ephemeral=True)
            return

        state = str(interaction.user.id)
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid",
            "state": state
        }
        auth_url = f"https://auth.riotgames.com/authorize?{urlencode(params)}"

        embed = discord.Embed(title="Riot 계정 로그인", description="아래 버튼을 눌러 로그인하세요.", color=0x1abc9c)
        view = View()
        view.add_item(Button(label="로그인", url=auth_url, style=discord.ButtonStyle.link))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # ---------- /riotinfo ----------
    @app_commands.command(name="riotinfo", description="로그인한 Riot 정보와 전적 확인")
    async def riotinfo(self, interaction: discord.Interaction):
        user_data = db.get_riot_user(str(interaction.user.id))
        if not user_data:
            await interaction.response.send_message("⚠️ 로그인 기록이 없습니다. `/riotlogin`으로 먼저 로그인하세요.", ephemeral=True)
            return

        summoner_name, access_token, refresh_token, token_expiry = user_data

        # 토큰 만료 체크
        if datetime.datetime.utcnow() > datetime.datetime.fromisoformat(token_expiry):
            await interaction.response.send_message("⚠️ 토큰이 만료되었습니다. `/riotlogin`으로 다시 로그인하세요.", ephemeral=True)
            return

        # Riot API 호출
        headers = {"Authorization": f"Bearer {access_token}"}
        summoner_data, match_data, valorant_store = {}, {}, {}

        async with aiohttp.ClientSession() as session:
            # 롤 소환사 정보
            async with session.get(f"https://REGION.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}", headers=headers) as resp:
                if resp.status == 200:
                    summoner_data = await resp.json()

            # 롤 최근 경기 (전적)
            async with session.get(f"https://REGION.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_data.get('puuid')}/ids?start=0&count=5", headers=headers) as resp:
                if resp.status == 200:
                    match_data = await resp.json()

            # 발로란트 상점 (예시)
            async with session.get("https://pd.NA.a.pvp.net/store/v2/storefront/", headers=headers) as resp:
                if resp.status == 200:
                    valorant_store = await resp.json()

        embed = discord.Embed(title=f"{summoner_name} 정보", color=0x3498db)
        embed.add_field(name="소환사명", value=summoner_name, inline=False)
        embed.add_field(name="최근 전적", value=str(match_data[:5]), inline=False)
        embed.add_field(name="발로란트 상점", value=str(valorant_store.get("SkinsPanelLayout")), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RiotCog(bot))
