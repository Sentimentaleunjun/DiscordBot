import discord
from discord.ext import commands
from discord import app_commands

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notes = [
            "🎉 따까리봇 1.0.1",
            "📅 출시일: 2025-09-10",
            "✨ 슬래시 명령어 완전 지원: /help, /userinfo, /dm, /support, /schedule, /addschedule, /dblookup, /loglookup 등",
            "🎮 펀(Fun) 기능 강화: /rps, /points, /quiz 등",
            "🌐 서버 상태 표시 개선: Presence 자동 업데이트로 현재 봇이 들어간 서버 수 기준",
            "📚 헬프(Help) 기능 개선: 귀여운 임베드, 카테고리별 명령어, 개발사 링크 포함",
            "🗄 DB 기능 안정화: 포인트 관리, 스케줄 관리, 로그 조회, 데이터 조회",
            "🛠 버그 수정 및 안정성 강화",
            "⚡ 에러 핸들링 강화 및 UI/UX 개선",
            "🔧 코그 구조 최적화 및 통합",
            "🚀 서버 관리 상태 표시 개선: '36개의 서버 관리중 🔥' 등 실시간 업데이트",
            "💖 사용자 편의성 향상: 명령어 반응 개선 및 피드백 반영"
        ]

    @app_commands.command(name="patchnote", description="따까리봇 1.0 정식 출시 패치노트를 확인합니다.")
    async def patchnote(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📢 따까리봇 1.0 패치노트",
            description="\n".join(self.notes),
            color=discord.Color.purple()
        )
        embed.set_footer(text="Edited by Flow in GSEJ 💖")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))
