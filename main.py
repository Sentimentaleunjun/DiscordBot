# -*- coding: utf-8 -*-
import threading
from takkari_bot.main_bot import run_discord_bot
from support_web.app import run_web

def run_bot():
    run_discord_bot()

def run_flask():
    run_web()

if __name__ == "__main__":
    # 웹 서버와 디스코드 봇을 동시에 실행
    t1 = threading.Thread(target=run_flask)
    t1.start()

    run_bot()
