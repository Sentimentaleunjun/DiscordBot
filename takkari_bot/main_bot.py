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
    print(f"??濡쒓렇???꾨즺: {bot.user}")


@bot.event
async def setup_hook():
    """cogs ?먮룞 濡쒕뱶"""
    import os
    for filename in os.listdir("./takkari_bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"takkari_bot.cogs.{filename[:-3]}")


def run_discord_bot():
    """?몃??먯꽌 ?ㅽ뻾"""
    if not TOKEN:
        raise ValueError("??DISCORD_TOKEN ?섍꼍蹂?섍? ?ㅼ젙?섏? ?딆븯?듬땲??")
    bot.run(TOKEN)

