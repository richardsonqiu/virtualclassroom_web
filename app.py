from flask import Flask, request, session, redirect, render_template, jsonify, flash

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
