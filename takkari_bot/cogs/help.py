# takkari_bot/cogs/help.py
import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="봇 명령어 목록을 보여줍니다!")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 따까리봇 소개 및 사용가이드",
            description="More convenient, Safer! 여러분들의 잡일 해결봇 따까리봇입니다!✨\n봇에게 고칠 사항이나 오류가 발견되면 DM으로 문의주세요!",
            color=0xC3073F
        )

        embed.add_field(name="📅 스케줄", value="/addschedule (관리자 전용) → 서버 전체 일정 등록\n/schedule → 일정 확인", inline=False)
        embed.add_field(name="🔍 데이터 조회", value="/dblookup (관리자 전용)\n/loglookup (관리자 전용)", inline=False)
        embed.add_field(name="📨 고객 지원", value="/support → 문의 등록\n/supportlist (개발자 전용)", inline=False)
        embed.add_field(name="⚙️ 기타", value="/userinfo @유저\n/dm @유저 <메시지> (관리자)", inline=False)
        embed.add_field(name="🎉 펀(Fun) 기능", value="/rps → 가위바위보 게임\n/points → 내 포인트 확인\n/quiz → 퀴즈 출제 및 풀기", inline=False)
        embed.add_field(name="🌐 개발사", value="[GSEJ Company](https://gsej-company.onrender.com)", inline=False)
        embed.set_footer(text="Edited by Flow in GSEJ 💖")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
