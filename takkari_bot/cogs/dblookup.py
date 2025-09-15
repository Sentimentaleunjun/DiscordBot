import discord
from discord import app_commands
from discord.ext import commands

# 운영진 역할 ID
ADMIN_ROLE_IDS = [1416769872284876931 , 1416769282380922991]

# DB조회 채널 ID
DB_CHANNEL_ID = 1417052678378360914 # 운영진 DB조회 채널 ID

class DBLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dblookup", description="운영진 전용: DB에서 정보를 조회합니다.")
    async def dblookup(self, interaction: discord.Interaction, query: str):
        member = interaction.user

        # 운영진 체크
        if not any(role.id in ADMIN_ROLE_IDS for role in member.roles):
            await interaction.response.send_message("❌ 운영진만 사용 가능한 명령어입니다.", ephemeral=True)
            return

        # DB 조회 로직 (예시)
        result = f"'{query}' 검색 결과: 예시 데이터"

        # DB조회 채널 가져오기
        db_channel = interaction.guild.get_channel(DB_CHANNEL_ID)
        if db_channel is None:
            await interaction.response.send_message("❌ DB조회 채널을 찾을 수 없습니다.", ephemeral=True)
            return

        # 채널에 결과 전송
        await db_channel.send(f"📌 {member.mention}님이 조회한 DB 결과:\n```{result}```")

        # 명령어 사용자는 ephemeral로 안내
        await interaction.response.send_message(f"✅ DB조회가 완료되었습니다. <#{DB_CHANNEL_ID}> 채널에서 결과를 확인하세요.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DBLookup(bot))