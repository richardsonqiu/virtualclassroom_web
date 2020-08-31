from flask import Flask, request, session, redirect, render_template, jsonify, flash
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
from flask import g

import sqlite3

conn = sqlite3.connect('classroom.db', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)

app.secret_key = 'dev'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    # cur = get_db().cursor()
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    """ Register user """
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Check username submitted
        username = request.form.get("username")
        if not username:
            return render_template("error.html", message="please provide username")

        # Check if username already exists
        username_check = cursor.execute("SELECT * FROM user WHERE username=:username", {"username": username}).fetchone()
        if username_check:
            return render_template("error.html", message="username already exists")

        # Check password submitted
        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="please provide password")

        # Check confirmation password submitted
        confirm_password = request.form.get("confirm_password")
        if not confirm_password:
            return render_template("error.html", message="please provide confirmation password")

        # Check passwords are equal
        if not password == confirm_password:
            return render_template("error.html", message="passwords did not match")

        # Hash password to store in DB , method='pbkdf2:sha256', salt_length=8
        hashed_password = generate_password_hash(password)

        # Insert registered user into DB
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                       (username, hashed_password))

        conn.commit()

        flash("Account created", 'info')

        return redirect("/login")


@app.route("/login")
def login():
    """ Log user in """
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("error.html", message="please provide username")
        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="please provide password")

        rows = cursor.execute("SELECT * FROM user WHERE username= ?", username)

        result = rows.fetchone()

        # check username exists and password correct
        if result == None or not check_password_hash(result[2], password):
            return render_template("error.html", message="invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = result[0]
        session["user_username"] = result[1]
        print(result[0])
        print(result[1])

        # redirect user to home page again
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """ Log user out """
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run()
