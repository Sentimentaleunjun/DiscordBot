import discord
from discord.ext import tasks
import asyncio
from flask import Flask
import os

# ------------------ Discord Bot 설정 ------------------
intents = discord.Intents.default()
intents.message_content = True  # 필요에 따라 True/False 조정

bot = discord.Bot(intents=intents)  # 슬래시 전용

# ------------------ Presence 상태 ------------------
@tasks.loop(seconds=10)
async def change_presence():
    guild_count = len(bot.guilds)
    statuses = [
        f"🔥 {guild_count}개의 서버 관리중",
        "🚀 업데이트 준비",
        "🤖 AI로 코딩"
    ]
    for status in statuses:
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

# Render에서는 PORT 환경변수를 사용
port = int(os.environ.get("PORT", 10000))

# ------------------ 봇 이벤트 ------------------
@bot.event
async def on_ready():
    print(f"{bot.user} 봇 로그인 완료")
    change_presence.start()  # Presence 상태 시작
    await load_all_cogs()

# ------------------ 메인 ------------------
if __name__ == "__main__":
    # Flask 서버 비동기 실행
    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=port)
    Thread(target=run_flask).start()

    # 디스코드 봇 실행
    bot.run(os.environ["DISCORD_BOT_TOKEN"])