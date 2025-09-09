# main.py
import discord
from discord.ext import commands, tasks
from itertools import cycle
from takkari_bot.utils import db

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# 상태 메시지 초기화 (첫 번째 메시지는 서버 수를 나중에 업데이트)
status_messages = [
    "",  # 서버 수가 들어갈 자리
    "정식출시 준비중🚀",
    "🤖AI로 코딩중"
]
status_cycle = None  # cycle 객체는 on_ready에서 생성

@bot.event
async def on_ready():
    global status_cycle
    print(f"✅ Bot logged in as {bot.user}!")
    
    # 서버 수를 첫 번째 메시지에 반영
    status_messages[0] = f"{len(bot.guilds)}개의 서버 관리중 🔥"
    status_cycle = cycle(status_messages)

    change_status.start()
    
    # 슬래시 커맨드 동기화
    await bot.tree.sync()
    print(f"✅ 현재 {len(bot.guilds)}개의 서버에서 활동 중!")

# 상태 메시지 변경
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))

# ---------------- Cog 로딩 ----------------
initial_extensions = [
    "takkari_bot.cogs.help",
    "takkari_bot.cogs.schedule",
    "takkari_bot.cogs.patchnote",
    "takkari_bot.cogs.support",
    "takkari_bot.cogs.userinfo",
    "takkari_bot.cogs.db_lookup",
    "takkari_bot.cogs.loglookup",
    "takkari_bot.cogs.dm_feature",
    "takkari_bot.cogs.accordingtobot",
    "takkari_bot.cogs.fun"
]

if __name__ == "__main__":
    for ext in initial_extensions:
        bot.load_extension(ext)

    bot.run("YOUR_BOT_TOKEN")
