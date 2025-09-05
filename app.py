from flask import Flask, render_template, jsonify
from support_web.utils.db import get_support_data

app = Flask(__name__, template_folder="support_web/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/support")
def support_api():
    data = get_support_data()  # DB에서 문의 데이터 가져오기
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
