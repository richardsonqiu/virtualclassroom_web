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

with app.app_context():
    player = Player.query.filter_by(username='a').first()
    player.balance = 5000
    player.current_avatar = 'vBasicController_MiniGirl'
    db.session.commit()
