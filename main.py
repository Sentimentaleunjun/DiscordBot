import discord
from discord.ext import commands, tasks
from flask import Flask
import os
import asyncio
from threading import Thread

# ------------------ Discord Bot 설정 ------------------
intents = discord.Intents.default()
intents.message_content = True  # 필요에 따라 True/False 조정

bot = commands.Bot(command_prefix="/", intents=intents)  # 슬래시 전용
tree = bot.tree  # 슬래시 명령어 등록용

# ------------------ Presence 상태 ------------------
statuses = [
    "🚀 업데이트 준비",
    "🤖 AI로 코딩"
]

@tasks.loop(seconds=10)
async def change_presence():
    guild_count = len(bot.guilds)
    # 서버 수를 포함한 첫 번째 상태
    dynamic_statuses = [f"🔥 {guild_count}개의 서버 관리중"] + statuses
    for status in dynamic_statuses:
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(10)

# ------------------ Cog 로드 ------------------
cogs = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.fun",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.accordingtobot"
]

async def load_all_cogs():
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ {cog} 로드 완료")
        except Exception as e:
            print(f"❌ {cog} 로드 실패: {e}")

# ------------------ Flask 서버 설정 ------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "봇 서버가 실행 중입니다!"

port = int(os.environ.get("PORT", 10000))

def run_flask():
    app.run(host="0.0.0.0", port=port)

# ------------------ 봇 이벤트 ------------------
@bot.event
async def on_ready():
    print(f"{bot.user} 봇 로그인 완료")
    change_presence.start()  # Presence 상태 시작
    await load_all_cogs()
    await tree.sync()  # 슬래시 명령어 글로벌 동기화
    print("🌐 슬래시 명령어 글로벌 동기화 완료")

# ------------------ 메인 ------------------
if __name__ == "__main__":
    Thread(target=run_flask).start()  # Flask 서버 백그라운드 실행
    bot.run(os.environ["DISCORD_BOT_TOKEN"])