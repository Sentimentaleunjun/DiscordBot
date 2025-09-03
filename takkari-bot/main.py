import discord
from discord.ext import commands
from flask import Flask, render_template, request, redirect, session
import threading, os, sqlite3
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- SQLite 초기화 ---
os.makedirs("db", exist_ok=True)
conn = sqlite3.connect("db/bot.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, message TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS patchnotes (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT)")
conn.commit()
conn.close()

# --- Flask 웹 ---
app = Flask(__name__)
app.secret_key = "supersecret"  # 세션용 임시 키

@app.route("/")
def index():
    if "logged_in" in session:
        conn = sqlite3.connect("db/bot.db")
        cur = conn.cursor()
        cur.execute("SELECT id, user, message FROM tickets ORDER BY id DESC")
        tickets = cur.fetchall()
        conn.close()
        return render_template("tickets.html", tickets=tickets)
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/")
    return render_template("login.html")

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

# --- Cog 로드 ---
initial_cogs = ["cogs.help_cmd", "cogs.dblookup", "cogs.patch_notes", "cogs.support"]

@bot.event
async def on_ready():
    for cog in initial_cogs:
        await bot.load_extension(cog)
    print(f"✅ 봇 로그인 완료: {bot.user}")

@bot.command()
async def restart(ctx):
    if ctx.author.id != DEVELOPER_ID:
        await ctx.send("❌ 이 명령어는 GSEJ Developer만 사용할 수 있습니다.")
        return
    await ctx.send("♻️ 봇을 재시작합니다...")
    await bot.close()

bot.run(TOKEN)
