# main.py
# -*- coding: utf-8 -*-
import threading
from support_web.app import run_web
from takkari_bot.main_bot import run_discord_bot

def run_bot():
    run_discord_bot()

if __name__ == "__main__":
    # Flask 웹 서버를 별도 스레드에서 실행
    t = threading.Thread(target=run_web)
    t.start()

    # Discord 봇 실행
    run_bot()
