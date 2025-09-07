import discord
from discord import app_commands
from discord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇 사용 가이드")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 따까리봇 소개 및 사용가이드",
            description="More convenient, Safer! 여러분들의 잡일 해결봇 따까리봇입니다!\n"
                        "봇에게 고칠 사항이나 오류가 발견되면 eunddiseundd#0으로 DM 주시거나 `/support`를 통해 문의해주세요!",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="📅 스케줄",
            value="/addschedule (관리자 전용기능) → 서버 전체 일정 등록\n"
                  "/schedule → 일정 확인",
            inline=False
        )
        embed.add_field(
            name="🔍 데이터 조회",
            value="/dblookup (관리자 전용 기능)\n"
                  "/loglookup (관리자 전용 기능)",
            inline=False
        )
        embed.add_field(
            name="📨 고객 지원",
            value="/support → 문의 등록\n"
                  "/supportlist (개발자 전용 기능)",
            inline=False
        )
        embed.add_field(
            name="⚙️ 기타",
            value="/userinfo @유저\n"
                  "/dm @유저 <메시지> (관리자)",
            inline=False
        )
        embed.add_field(
            name="🌐 개발사",
            value="[GSEJ Company](https://gsej-company.onrender.com)",
            inline=False
        )
        embed.set_footer(text="Edited by Flow in GSEJ")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
