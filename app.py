from flask import Flask, request, session, redirect, render_template, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from werkzeug.security import check_password_hash, generate_password_hash

import os, sqlite3


# Set up db
from models import Player, ShopItem, PlayerItem, Item, db

# Load env variables
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return render_template("error.html", message="please provide username")

        username_check = Player.query.filter_by(username=username).first()
        if username_check:
            return render_template("error.html", message="username already exists")

        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="please provide password")

        confirm_password = request.form.get("confirm_password")
        if not confirm_password:
            return render_template("error.html", message="please provide confirmation password")

        if not password == confirm_password:
            return render_template("error.html", message="passwords did not match")

        player = Player(username=username, password=password)
        db.session.add(player)
        db.session.commit()
        flash("Account created", 'info')

        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("error.html", message="please provide username")
        
        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="please provide password")

        player = Player.query.filter_by(username=username).first()

        if player is None:
            return render_template("error.html", message="boop")

        # remember which user has logged in
        session["player_id"] = player.id
        session["username"] = player.username

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/shop", methods=["GET", "POST"])
def shop():
    player_id = session["player_id"]
    player = Player.query.filter_by(id=player_id).first()

    if request.method == "GET":
        shopItems = ShopItem.query.all()
        return render_template("shop.html", shopItems=shopItems, balance=player.balance)
    else:
        item_id = request.form.get("itemId")
        item = Item.query.filter_by(id=item_id).first()

        if player.balance < item.price:
            return render_template("error.html", message="not enough money")

        player.balance -= item.price
        db.session.commit()

        return redirect("/shop")

@app.route("/avatarshop")
def avatarshop():
    currentPlayer = session["player_id"]
    if request.method == "GET":
        shopItems = cursor.execute("SELECT * FROM ShopItem").fetchall()
        if shopItems:
            print(shopItems)

        currency = cursor.execute("SELECT * FROM Players WHERE playerId=?", [currentPlayer]).fetchone()
        return render_template("avatarshop.html", shopItems=shopItems, currency=currency)
    else:
        buy = int(request.form.get("buy"))
        currentMoney = cursor.execute("SELECT currency FROM Players WHERE playerId=?", [currentPlayer]).fetchone()
        currentMoney = currentMoney[0]
        if currentMoney < buy:
            return render_template("error.html", message="Not enough money")

        currency = cursor.execute("UPDATE Players SET currency = currency - ? WHERE playerId=?", [buy, currentPlayer]).fetchone()
        conn.commit()
        return redirect("/avatarshop")

if __name__ == '__main__':
    app.run(debug=True)
