import os
import discord
from discord.ext import commands
from flask import Flask
from takkari_bot.utils import db

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)  # 슬래시 전용

# DB 초기화
db.init_db()

# Cog 로드
cogs = [
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.addschedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.help"
]

for cog in cogs:
    bot.load_extension(cog)
    print(f"✅ {cog} 로드 완료")

# 봇 상태
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"🔥 {len(bot.guilds)}개의 서버 관리중, 🚀 업데이트 준비, 🤖 AI로 코딩하는중"
        )
    )
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)}개 글로벌 슬래시 명령어 동기화 완료")
    except Exception as e:
        print(f"❌ 슬래시 동기화 오류: {e}")
    print(f"{bot.user} 로그인 완료!")

# Flask 서버
app = Flask("takkari_bot")

@app.route("/")
def home():
    return "봇이 실행 중입니다!"

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])