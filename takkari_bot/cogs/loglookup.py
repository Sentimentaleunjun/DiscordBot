import discord
from discord.ext import commands
from discord import app_commands

class LogLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loglookup", description="현재 채널에서 채팅 로그를 검색합니다.")
    async def loglookup(self, interaction: discord.Interaction, keyword: str):
        channel = interaction.channel
        found_messages = []

        async for msg in channel.history(limit=100):  # 최근 100개 메시지 검색
            if keyword.lower() in msg.content.lower():
                found_messages.append(f"[{msg.author.display_name}] {msg.content}")

        if not found_messages:
            await interaction.response.send_message(f"❌ '{keyword}' 에 대한 검색 결과가 없습니다.", ephemeral=True)
        else:
            result = "\n".join(found_messages[:10])  # 최대 10개까지만 보여줌
            embed = discord.Embed(
                title=f"🔍 '{keyword}' 검색 결과",
                description=result,
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(LogLookup(bot))
