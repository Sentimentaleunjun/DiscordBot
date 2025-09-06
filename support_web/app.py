# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "따까리봇 웹 대시보드 실행 중 ✅"

def run_web():
    import os
    port = int(os.environ.get("PORT", 10000))  # Render 기본 포트 환경변수
    app.run(host="0.0.0.0", port=port)
