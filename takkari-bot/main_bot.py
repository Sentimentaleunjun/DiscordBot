import os
import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")


@bot.event
async def setup_hook():
    """cogs 자동 로드"""
    import os
    for filename in os.listdir("./takkari_bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"takkari_bot.cogs.{filename[:-3]}")


def run_discord_bot():
    """외부에서 실행"""
    if not TOKEN:
        raise ValueError("❌ DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")
    bot.run(TOKEN)

