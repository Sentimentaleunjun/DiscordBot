from flask import Flask, render_template, jsonify
from utils.db import get_support_data

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/support")
def support_api():
    data = get_support_data()  # DB에서 문의 불러오기
    return jsonify(data)
