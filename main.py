import os
import threading
from flask import Flask
import discord
from discord import app_commands

# ---------------------------
# 환경 변수
# ---------------------------
TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_TOKEN")  # Render 환경 변수 권장
PORT = int(os.getenv("PORT", "10000"))            # Render 포트
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID", "0"))  # 테스트 서버 ID

# ---------------------------
# Flask 웹 서버
# ---------------------------
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Takkari Bot Dashboard is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

# ---------------------------
# Discord 봇
# ---------------------------
intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # 코그 로드 (경로 수정됨)
        for ext in (
            "takkari_bot.cogs.help",
            "takkari_bot.cogs.schedule",
            "takkari_bot.cogs.patchnote",
            "takkari_bot.cogs.db_lookup",
            "takkari_bot.cogs.accordingtobot",
        ):
            try:
                await self.load_extension(ext)
                print(f"[cog] loaded: {ext}")
            except Exception as e:
                print(f"[cog] skip {ext}: {e}")

        # 슬래시 명령어 동기화
        if TEST_GUILD_ID:
            await self.tree.sync(guild=discord.Object(id=TEST_GUILD_ID))
            print(f"[slash] synced to test guild: {TEST_GUILD_ID}")
        else:
            await self.tree.sync()
            print("[slash] synced globally")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (ID: {self.user.id})")

# ---------------------------
# 실행
# ---------------------------
if __name__ == "__main__":
    # Flask는 쓰레드로 실행
    web_thread = threading.Thread(target=run_web)
    web_thread.start()

    # Discord 봇 실행
    client = MyClient()
    client.run(TOKEN)
