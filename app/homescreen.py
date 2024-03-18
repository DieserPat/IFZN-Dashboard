from app import app
from flask import render_template

@app.route("/")
def start():
    return render_template("start.html")