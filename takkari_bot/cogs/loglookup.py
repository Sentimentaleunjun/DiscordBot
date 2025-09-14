# loglookup.py
import discord
from discord.ext import commands
from discord import app_commands

class LogLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loglookup", description="현재 채널에서 채팅 로그를 검색합니다.")
    async def loglookup(self, interaction: discord.Interaction, keyword: str):
        channel = interaction.channel
        found = []

        # 일부 환경에선 오래된 메시지/내용 접근이 제한될 수 있어 예외 대비
        try:
            async for msg in channel.history(limit=200):  # 최근 200개
                content = msg.content or ""
                if keyword.lower() in content.lower():
                    found.append(f"[{msg.author.display_name}] {content}")
        except Exception as e:
            await interaction.response.send_message(
                f"TKR 004 오류 , 로그 접근 중 오류가 발생했습니다: {type(e).__name__}", ephemeral=True
            )
            return

        if not found:
            await interaction.response.send_message(f"❌ '{keyword}' 에 대한 검색 결과가 없습니다.", ephemeral=True)
        else:
            result = "\n".join(found[:10])  # 최대 10개
            embed = discord.Embed(title=f"🔍 '{keyword}' 검색 결과", description=result, color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(LogLookup(bot))
