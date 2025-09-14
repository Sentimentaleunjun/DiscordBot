# takkari_bot/cogs/help.py
import discord
from discord.ext import commands
from discord import app_commands

HELP_PAGES = [
    {
        "title": "ℹ️ 유저 / 공지",
        "color": discord.Color.blue(),
        "commands": [
            ("/userinfo", "유저 정보를 확인합니다."),
            ("/announce", "원하는 채널에 공지를 봇을 통해 등록합니다.")
        ]
    },
    {
        "title": "🛠️ 지원 / 일정",
        "color": discord.Color.green(),
        "commands": [
            ("/support", "봇 고객지원 요청을 보냅니다."),
            ("/schedule", "일정을 추가/조회합니다.")
        ]
    },
    {
        "title": "🎮 게임 / 로그",
        "color": discord.Color.blurple(),
        "commands": [
            ("/riot", "라이엇 관련 기능을 사용합니다"),
            ("/loglookup", "서버 로그를 조회합니다"),
            ("/dblookup", "DB를 조회합니다")
        ]
    },
    {
        "title": "✉️ DM / 헬프",
        "color": discord.Color.light_grey(),
        "commands": [
            ("/dm", "봇을 통해 서버의 어느 사람에게 DM을 전송합니다"),
            ("/help", "이 도움말을 봅니다")
        ]
    }
]

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.page = 0
        self.update_buttons()

    def get_embed(self):
        page = HELP_PAGES[self.page]
        embed = discord.Embed(title=page["title"], color=page["color"])
        for cmd, desc in page["commands"]:
            embed.add_field(name=cmd, value=desc, inline=False)
        embed.set_footer(text=f"페이지 {self.page+1}/{len(HELP_PAGES)}")
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        return embed

    def update_buttons(self):
        # 버튼 초기화
        self.clear_items()
        # 이전 버튼
        self.add_item(discord.ui.Button(label="◀️ 이전", style=discord.ButtonStyle.secondary, custom_id="prev"))
        # 숫자 버튼
        for i in range(len(HELP_PAGES)):
            self.add_item(discord.ui.Button(label=str(i+1), style=discord.ButtonStyle.primary, custom_id=f"page_{i}"))
        # 다음 버튼
        self.add_item(discord.ui.Button(label="▶️ 다음", style=discord.ButtonStyle.secondary, custom_id="next"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # 모든 버튼 클릭 이벤트 처리
        if interaction.data["custom_id"] == "prev":
            self.page = (self.page - 1) % len(HELP_PAGES)
        elif interaction.data["custom_id"] == "next":
            self.page = (self.page + 1) % len(HELP_PAGES)
        elif interaction.data["custom_id"].startswith("page_"):
            self.page = int(interaction.data["custom_id"].split("_")[1])
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
        return False  # 기본 동작 막기


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="따까리봇 명령어와 안내 ✨")
    async def help(self, interaction: discord.Interaction):
        view = HelpView(self.bot)
        embed = view.get_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
