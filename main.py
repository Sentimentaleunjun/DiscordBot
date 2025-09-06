# -*- coding: utf-8 -*-
from takkari_bot.main_bot import run_discord_bot
from support_web.app import run_web

def run_bot():
    run_discord_bot()

if __name__ == "__main__":
    run_web()
    run_bot()
