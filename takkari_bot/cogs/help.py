import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    """따까리봇의 명령어 안내"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇의 명령어를 안내합니다 ✨")
    async def help(self, interaction: discord.Interaction):
        # 임베드 생성
        embed = discord.Embed(
            title="🤖 따까리봇 명령어 안내",
            description="아래 버튼을 눌러 카테고리별 명령어를 확인하세요!",
            color=discord.Color.blurple()
        )

        embed.add_field(name="📝 유저 관련", value="`/userinfo`, `/stats` 등", inline=False)
        embed.add_field(name="📢 공지/패치", value="`/announce`, `/patchnote`", inline=False)
        embed.add_field(name="💌 DM 기능", value="`/dm_send`, `/dm_broadcast`", inline=False)
        embed.add_field(name="⚙️ 기타", value="`/updown`, `/dblookup`, `/schedule`", inline=False)

        # 버튼 뷰
        view = discord.ui.View()

        view.add_item(discord.ui.Button(label="유저 명령어", style=discord.ButtonStyle.primary, custom_id="help_user"))
        view.add_item(discord.ui.Button(label="공지/패치", style=discord.ButtonStyle.success, custom_id="help_announce"))
        view.add_item(discord.ui.Button(label="DM 기능", style=discord.ButtonStyle.secondary, custom_id="help_dm"))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# 버튼 클릭 이벤트 처리
class HelpButtonHandler(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="유저 명령어", style=discord.ButtonStyle.primary, custom_id="help_user")
    async def user_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📝 유저 명령어",
            description="유저 관련 명령어 목록입니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="/userinfo", value="사용자 정보를 확인합니다.", inline=False)
        embed.add_field(name="/stats", value="사용자 통계를 확인합니다.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="공지/패치", style=discord.ButtonStyle.success, custom_id="help_announce")
    async def announce_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📢 공지/패치",
            description="서버 공지 및 패치 관련 명령어입니다.",
            color=discord.Color.gold()
        )
        embed.add_field(name="/announce", value="공지사항을 작성합니다. (운영진 전용)", inline=False)
        embed.add_field(name="/patchnote", value="패치노트를 확인합니다.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="DM 기능", style=discord.ButtonStyle.secondary, custom_id="help_dm")
    async def dm_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💌 DM 기능",
            description="DM 발송 관련 명령어입니다.",
            color=discord.Color.blue()
        )
        embed.add_field(name="/dm_send", value="개별 DM을 발송합니다. (운영진 전용)", inline=False)
        embed.add_field(name="/dm_broadcast", value="전체 DM을 발송합니다. (운영진 전용)", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
    bot.add_view(HelpButtonHandler())  # 버튼 뷰 등록