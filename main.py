import os
import discord
from discord.ext import commands
import asyncio

# ===== 인텐트 설정 =====
intents = discord.Intents.default()
intents.message_content = True  # 메시지 컨텐츠 인텐트 허용

# ===== 봇 설정 =====
bot = commands.Bot(command_prefix="/", intents=intents)

# ===== 확장(코그) 목록 =====
extensions = [
    "takkari_bot.cogs.help",     # 헬프
    "takkari_bot.cogs.fun",      # 재미 기능 (rps, etc)
    "takkari_bot.cogs.admin",    # 관리자 기능
    "takkari_bot.cogs.db",     # DB 기능 (필요하면 켜기)
]

# ===== 이벤트 =====
@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")
    print(f"🤖 현재 {len(bot.guilds)}개의 서버에서 활동 중")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{len(bot.guilds)}개의 서버 관리중 🛠️")
    )

# ===== 코그 로드 =====
async def load_extensions():
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"🔌 Cog 로드 성공: {ext}")
        except Exception as e:
            print(f"❌ Cog 로드 실패: {ext} - {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.environ.get("DISCORD_TOKEN"))  # Render 환경변수 사용

if __name__ == "__main__":
    asyncio.run(main())
