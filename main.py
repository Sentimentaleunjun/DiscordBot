import os
import asyncio
from threading import Thread

# Discord Bot 불러오기
from takkari_bot.main_bot import run_discord_bot  

# Flask App 불러오기
from support_web.app import app  

# ----------------------------------------
# Flask 서버 실행
# ----------------------------------------
def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render는 PORT 환경변수를 자동 지정
    app.run(host="0.0.0.0", port=port)

# ----------------------------------------
# Discord Bot 실행 (비동기)
# ----------------------------------------
def run_bot():
    run_discord_bot()

# ----------------------------------------
# 실행부
# ----------------------------------------
if __name__ == "__main__":
    # Flask는 스레드로 실행
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 디스코드 봇 실행 (메인 이벤트 루프)
    run_bot()
