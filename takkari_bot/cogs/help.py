# takkari_bot/cogs/help.py
import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    """귀여운 슬래시 명령어 헬프 코그"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇의 모든 명령어 목록을 보여줘요! ✨")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 따까리봇 소개 및 사용가이드",
            description=(
                "여러분의 잡일 해결사! 🛠\n"
                "More convinent , Safer!✨\n"
                "오류나 개선 사항이 있다면 eunddiseundd#0 DM으로 알려주세요! 💌"
            ),
            color=0xC3073F
        )

        # 카테고리별 명령어
        embed.add_field(
            name="📅 스케줄",
            value="/addschedule → 서버 전체 일정 등록 (관리자 전용)\n/schedule → 일정 확인",
            inline=False
        )
        embed.add_field(
            name="🔍 데이터 조회",
            value="/dblookup → 데이터 조회 (관리자 전용)\n/loglookup → 로그 조회 (관리자 전용)",
            inline=False
        )
        embed.add_field(
            name="📨 고객 지원",
            value="/support → 문의 등록\n/supportlist → 문의 리스트 확인 (개발자 전용)",
            inline=False
        )
        embed.add_field(
            name="⚙️ 기타",
            value="/userinfo @유저 → 유저 정보 확인\n/dm @유저 <메시지> → DM 보내기 (관리자 전용)",
            inline=False
        )
        embed.add_field(
            name="🎉 Fun 기능",
            value="/rps → 가위바위보 게임\n/points → 내 포인트 확인\n/quiz → 퀴즈 출제 및 풀기",
            inline=False
        )
        embed.add_field(
            name="🌐 개발사",
            value="[GSEJ Company](https://gsej-company.onrender.com)",
            inline=False
        )

        embed.set_footer(text="Edited with 💖 by Flow in GSEJ")

        # Ephemeral 메시지로 보내서 오직 호출한 사람만 보이게
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))