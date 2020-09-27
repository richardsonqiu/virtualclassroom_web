from flask import Flask, request, session, redirect, render_template, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from werkzeug.security import check_password_hash, generate_password_hash

import os


# Set up db
from models import Player, ShopItem, PlayerItem, Item, db

# Load env variables
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()

# # shop_items = {
#     ('calculator', 10),
#     ('computer', 1000),
#     ('diary', 20),
#     ('highlighter', 50),
#     ('lectureNote', 30),
#     ('thumbdrive', 100)
# }
#

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

for x in shop_items:
    item = Item(name=x[0], category=x[1])
    shop_item = ShopItem(item=item, price=x[2])
    with app.app_context():
        db.session.add(item)
        db.session.add(shop_item)
        db.session.commit()