import os
import discord
from discord import app_commands
from discord.ext import commands

class RiotOAuth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="login_riot", description="라이엇 계정으로 로그인 💘")
    async def login_riot(self, interaction: discord.Interaction):
        client_id = os.environ.get("RIOT_CLIENT_ID")
        redirect_uri = os.environ.get("RIOT_REDIRECT_URI")
        if not client_id or not redirect_uri:
            await interaction.response.send_message(
                "TKR 001 오류. /support로 관리자에게 문의하세요",
                ephemeral=True
            )
            return

        oauth_url = (
            f"https://auth.riotgames.com/authorize"
            f"?client_id={client_id}"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}"
            f"&scope=openid%20account"
        )

        embed = discord.Embed(
            title="라이엇 로그인",
            description="아래 버튼을 눌러 Riot 계정으로 로그인하세요."
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="로그인", url=oauth_url))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(RiotOAuth(bot))