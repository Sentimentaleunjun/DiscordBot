import os
import discord
from discord.ext import commands
from flask import Flask, send_from_directory

# ===== Discord Bot =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# 샘플 커맨드
@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")

# ===== Flask Server =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

# Riot Verify TXT 파일 제공
@app.route("/riot/callback/riot.txt")
def serve_riot_file():
    return send_from_directory(os.getcwd(), "riot.txt")

# ===== Run both Bot + Flask =====
if __name__ == "__main__":
    from threading import Thread

    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

    def run_discord():
        bot.run(os.environ["DISCORD_TOKEN"])

    Thread(target=run_flask).start()
    run_discord()
