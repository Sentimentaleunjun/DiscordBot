import os
from threading import Thread
from takkari_bot.main_bot import run_discord_bot  

from support_web.app import app  


def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render媛 PORT ?먮룞 ?좊떦
    app.run(host="0.0.0.0", port=port)


def run_bot():
    run_discord_bot()


if __name__ == "__main__":
    
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    
    run_bot()
