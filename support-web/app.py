import os
from flask import Flask, render_template, request, redirect, session
from support_web.utils.db import get_supports

app = Flask(__name__)
app.secret_key = os.getenv("WEB_SECRET_KEY")

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["logged_in"] = True
            return redirect("/dashboard")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    data = get_supports()
    return render_template("dashboard.html", supports=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
