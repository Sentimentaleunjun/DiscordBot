# takkari_bot/cogs/patchnote.py
import discord
from discord import app_commands
from discord.ext import commands

# 패치노트 데이터 (버전별 기록 + 코드네임)
PATCHNOTES = {
    "0.9": {
        "codename": "Candidate Phoenix 🔥",
        "features": [
            "🗂️ 지원 시스템 → /support, /supportlist",
            "📅 스케줄 → /addschedule, /schedule",
            "📨 DM 기능 → /dm @유저 <메시지>",
            "🎯 포인트 & 퀴즈 시스템 안정성 검사 (0.9.1 정식 출시 예정)"
        ],
        "status": "공식 출시 임박 🎉 베타테스트 시작 👨‍💻👩‍💻"
    },
    "0.8": {
        "codename": "Beta Tiger 🐯",
        "features": [
            "🔍 DB 조회 기능 (/dblookup, /loglookup)",
            "👤 유저 정보 조회 (/userinfo)"
        ],
        "status": "Beta 테스트 완료"
    },
    "0.7": {
        "codename": "Alpha Falcon 🛠️",
        "features": [
            "🤖 기본 프레임워크 완성",
            "📜 /help 기능 추가"
        ],
        "status": "Alpha 단계"
    }
}

class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="patchnote", description="패치노트를 확인합니다.")
    @app_commands.describe(option="all 또는 특정 버전 입력 가능")
    async def patchnote(self, interaction: discord.Interaction, option: str = None):
        embed = discord.Embed(title="📢 패치노트", color=discord.Color.purple())
        
        if option is None:  # 최신 버전
            latest = sorted(PATCHNOTES.keys(), reverse=True)[0]
            data = PATCHNOTES[latest]
            embed.title += f" (최신: {latest} {data['codename']})"
            embed.description = "\n".join(data["features"]) + f"\n\n🧪 {data['status']}"
        
        elif option.lower() == "all":
            for ver, data in sorted(PATCHNOTES.items(), reverse=True):
                embed.add_field(
                    name=f"🚀 {ver} {data['codename']}",
                    value="\n".join(data["features"]) + f"\n🧪 {data['status']}",
                    inline=False
                )
        elif option in PATCHNOTES:
            data = PATCHNOTES[option]
            embed.title += f" ({option} {data['codename']})"
            embed.description = "\n".join(data["features"]) + f"\n\n🧪 {data['status']}"
        else:
            await interaction.response.send_message("❌ 해당 버전을 찾을 수 없습니다.", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PatchNote(bot))