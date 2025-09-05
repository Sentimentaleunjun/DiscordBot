import os
from threading import Thread

# Discord Bot 실행 함수
from takkari_bot.main_bot import run_discord_bot  

# Flask App
from support_web.app import app  


def run_flask():
    """Flask 웹 서버 실행"""
    port = int(os.environ.get("PORT", 5000))  # Render가 PORT 자동 할당
    app.run(host="0.0.0.0", port=port)


def run_bot():
    """Discord 봇 실행"""
    run_discord_bot()


if __name__ == "__main__":
    # Flask는 스레드로 실행
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 디스코드 봇 실행
    run_bot()
