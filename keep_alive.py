from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "봇 살아있음!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
