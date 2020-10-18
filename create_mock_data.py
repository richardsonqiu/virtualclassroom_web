from flask import Flask, request, session, redirect, render_template, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from werkzeug.security import check_password_hash, generate_password_hash

import os


# Set up db
from models import Player, ShopItem, PlayerItem, Item, Classroom, PlayerClassroom, db

# Load env variables
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()


shop_items = {
    ('av_allen', 'avatar', 500),
    ('av_allie', 'avatar', 500),
    ('av_ariel', 'avatar', 500),
    ('av_emilia', 'avatar', 500),
    ('av_michelle', 'avatar', 500),
    ('calculator', 'general', 10),
    ('computer', 'general', 1000),
    ('diary', 'general', 20),
    ('highlighter', 'general', 50),
    ('lecturenote', 'general', 30),
    ('thumbdrive', 'general', 100)
}

roomnames = [
    'ENGLISH',
    'MATH',
    'SCIENCE',
    'ART',
    'MOTHER TONGUE LANGUAGE',
    'PHYSICAL EDUCATION :)'
]

with app.app_context():
    for x in shop_items:
        item = Item(name=x[0], category=x[1])
        shop_item = ShopItem(item=item, price=x[2])
        db.session.add(item)
        db.session.add(shop_item)

    for roomname in roomnames:
        classroom = Classroom(roomname=roomname)
        db.session.add(classroom)

    player = Player('a', 'a')
    player.balance = 5000

    db.session.add(player)
    db.session.commit()
