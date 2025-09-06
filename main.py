import os
from threading import Thread
from takkari_bot.main_bot import run_discord_bot

# Discord Bot ?ㅽ뻾 ?⑥닔
from takkari_bot.main_bot import run_discord_bot  

# Flask App
from support_web.app import app  


def run_flask():
    """Flask ???쒕쾭 ?ㅽ뻾"""
    port = int(os.environ.get("PORT", 5000))  # Render媛 PORT ?먮룞 ?좊떦
    app.run(host="0.0.0.0", port=port)


def run_bot():
    """Discord 遊??ㅽ뻾"""
    run_discord_bot()


if __name__ == "__main__":
    # Flask???ㅻ젅?쒕줈 ?ㅽ뻾
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # ?붿뒪肄붾뱶 遊??ㅽ뻾
    run_bot()
