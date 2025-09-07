import discord
from discord.ext import commands
from discord import app_commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇 사용 가이드")
    async def help_command(self, interaction: discord.Interaction):
        # 먼저 defer 해서 타임아웃 방지
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🤖 따까리봇 소개 및 도움말",
            description="More Convenient, Safer! 안녕하세요 여러분의 잡일해결봇! 따까리봇 입니다!",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="📅 스케줄",
            value="`/addschedule` → 일정 추가\n`/schedule` → 일정 확인",
            inline=False
        )
        embed.add_field(
            name="🔍 데이터 조회",
            value="`/dblookup`\n`/loglookup`",
            inline=False
        )
        embed.add_field(
            name="📨 고객 지원",
            value="`/support` → 문의 등록\n`/supportlist` (개발자만)",
            inline=False
        )
        embed.add_field(
            name="⚙️ 기타",
            value="`/userinfo @유저`\n`/dm @유저 <메시지>` (관리자)",
            inline=False
        )
        embed.add_field(
            name="🌐 개발사",
            value="[GSEJ Company](https://gsej-company.onrender.com)",
            inline=False
        )
         embed.add_field(
            name="👨‍💻 개발자",
            value="Maker : Flow , Kbc",
            inline=False
        )
        # followup으로 최종 메세지 전송
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
