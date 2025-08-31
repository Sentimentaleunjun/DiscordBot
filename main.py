import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

client = MyClient()


@client.tree.command(name="help", description="따까리 봇 설명")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📌 따까리봇 사용 안내",
        description=(
            "안녕하세요! 따까리봇은 서버의 여러 잡일을 대신 처리해주는 **다용도 봇**입니다.\n\n"
            "🌐 [공식 웹사이트 바로가기](https://gsej-company.onrender.com)"
        ),
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ `/help`", value="따까리봇 도움말을 확인합니다", inline=False)
    embed.add_field(name="✅ `/accordingtobot [메시지]`", value="서버에 공지를 전송합니다 (관리자 전용)", inline=False)

    embed.set_thumbnail(url=interaction.client.user.display_avatar.url)  # 봇 프로필 사진
    embed.set_footer(text="앞으로 더 많은 기능이 추가될 예정이에요 🚀")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🌐 공식 웹사이트", url="https://gsej-company.onrender.com"))

    await interaction.response.send_message(embed=embed, view=view)


@client.tree.command(name="accordingtobot", description="서버에 공지를 전송합니다 (관리자 전용)")
@app_commands.describe(message="전송할 공지 내용을 입력하세요")
async def accordingtobot(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ 관리자만 사용할 수 있습니다.", ephemeral=True)
        return
    channel = discord.utils.get(interaction.guild.text_channels, name="공지")
    if channel is None:
        await interaction.response.send_message("❌ 공지 채널을 찾을 수 없습니다.", ephemeral=True)
        return
    await channel.send(f"📢 공지: {message}")
    await interaction.response.send_message(f"✅ 공지가 {channel.mention} 채널에 전송되었습니다.", ephemeral=True)


@client.event
async def on_ready():
    if not client.synced:
        await client.tree.sync()
        client.synced = True
    print(f"✅ 봇 로그인 완료: {client.user} (ID: {client.user.id})")


client.run("MTQwODcyNDU4OTc3NjczNjM1Nw.GwjTpK.H91Fib_F04U3Sdi4ZZyB0o6wkxocJ0ebNn0dKg")
