# support_web/app.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template_string
from takkari_bot.utils.db import get_supports, init_db

app = Flask(__name__)

# DB 초기화
init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>지원 요청 대시보드</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1>지원 요청 목록</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>유저 ID</th>
            <th>메시지</th>
            <th>생성 시간</th>
        </tr>
        {% for row in supports %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    supports = get_supports()
    return render_template_string(HTML_TEMPLATE, supports=supports)

def run_web():
    app.run(host="0.0.0.0", port=10000)
