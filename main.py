import os
import threading
import asyncio
import sys
import uvicorn

# ---------------------------------
# support_web (Flask/FastAPI) 불러오기
# ---------------------------------
from support_web.app import app

# ---------------------------------
# takkari-bot 불러오기
# (utils, cogs 인식 가능하게 경로 추가)
# ---------------------------------
sys.path.append("takkari-bot")
from main import run_bot   # takkari-bot/main.py 안에 run_bot() 함수 있어야 함

# ---------------------------------
# 웹 서버 실행
# ---------------------------------
def start_web():
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# ---------------------------------
# 메인 실행
# ---------------------------------
if __name__ == "__main__":
    # 웹 서버는 별도 쓰레드로 실행
    web_thread = threading.Thread(target=start_web, daemon=True)
    web_thread.start()

    # 디스코드 봇 실행
    asyncio.run(run_bot())
