import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 카테고리별 일반 사용자 명령어
        self.commands_info = {
            "정보": {
                "userinfo": "유저 정보를 확인합니다."
            },
            "소통": {
                "announce": "공지사항을 등록합니다.",
                "support": "문의/피드백을 등록합니다.",
                "dm": "서버 구성원에게 DM 전송"
            },
            "업데이트/기타": {
                "schedule": "일정을 확인/등록합니다.",
                "patchnote": "업데이트 내용을 확인합니다.",
                "loglookup": "로그를 조회합니다.",
                "riot": "라이엇 관련 명령어",
                "help": "명령어 목록을 확인합니다."
            }
        }

    @app_commands.command(name="help", description="봇 명령어 목록을 확인합니다.")
    async def help(self, interaction: discord.Interaction):
        help_text = "📜 **따까리봇 일반 사용자 명령어 목록** 📜\n\n"
        for category, cmds in self.commands_info.items():
            help_text += f"**{category}**\n"
            for cmd, desc in cmds.items():
                help_text += f"  • **/{cmd}** - {desc}\n"
            help_text += "\n"

        await interaction.response.send_message(help_text, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))