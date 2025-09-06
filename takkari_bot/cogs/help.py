from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="사용 가능한 명령어 목록 보기")
    async def help(self, interaction):
        await interaction.response.send_message(
            "📌 사용 가능한 명령어:\n"
            "/userinfo - 유저 정보 보기\n"
            "/loglookup - 로그 검색\n"
            "/schedule - 예약 관리\n"
            "/patchnote - 패치노트 확인\n"
            "/support - 고객지원 등록\n",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
