import os
import threading
import discord
from discord.ext import commands
from flask import Flask, render_template
from takkari_bot.utils.db import init_db   # ✅ utils → takkari_bot.utils 로 변경

# --- Flask ---
app = Flask(__name__, template_folder="support-web/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# --- Discord Bot ---
TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("DEV_ID", "0"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

init_db()

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user}")

for filename in os.listdir("./takkari-bot/cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"takkari-bot.cogs.{filename[:-3]}")

# --- Run ---
def run_discord_bot():
    bot.run(TOKEN)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run_discord_bot).start()
    run_flask()