from flask import Flask, request, session, redirect, render_template, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

import json
import os


# Set up db
from models import Player, ShopItem, PlayerItem, Item, Classroom, PlayerClassroom, db

# Load env variables
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        if not username:
            return render_template('error.html', message='please provide username')

        username_check = Player.query.filter_by(username=username).first()
        if username_check:
            return render_template('error.html', message='username already exists')

        password = request.form.get('password')
        if not password:
            return render_template('error.html', message='please provide password')

        confirm_password = request.form.get('confirm_password')
        if not confirm_password:
            return render_template('error.html', message='please provide confirmation password')

        if not password == confirm_password:
            return render_template('error.html', message='passwords did not match')

        player = Player(username=username, password=password)
        db.session.add(player)

        classrooms = Classroom.query.all()
        for classroom in classrooms:
            player_classroom = PlayerClassroom(classroom=classroom, player=player)
            db.session.add(player_classroom)

        db.session.commit()
        flash('Account created', 'info')

        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        player = Player.query.filter_by(username=username).first()
        
        # remember which user has logged in
        session['player_id'] = player.id
        session['username'] = player.username

        if player and player.check_password(password):
            return jsonify({
                'status': 'Ok',
                'data': {
                    'roomnames': player.get_roomnames()
                }
            })
        else:
            return jsonify({
                'status': 'Error',
                'data': {
                    'message': 'Invalid username or password.'
                }
            })

    else:
        return render_template('login.html')

@app.route('/joinroom', methods=['POST'])
def joinroom():
    player = Player.query.filter_by(username=session['username']).first()
    roomname = request.json.get('roomname')
    return jsonify({
        'status': 'Ok',
        'data': {
            'username': player.username,
            'roomname': roomname,
            'avatar': player.current_avatar
        }
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    player_id = session['player_id']
    player = Player.query.filter_by(id=player_id).first()

    if request.method == 'GET':
        shopItems = ShopItem.query.join(ShopItem.item).filter(Item.category == 'general').all()
        return render_template('shop.html', shopItems=shopItems, balance=player.balance)
    else:
        shop_item_id = request.form.get('itemId')
        shop_item = ShopItem.query.filter_by(id=shop_item_id).first()

        if player.balance < shop_item.price:
            return render_template('error.html', message='not enough money')

        player.balance -= shop_item.price
        player_item = PlayerItem(item=shop_item.item, player=player)
        db.session.add(player_item)
        db.session.commit()

        return redirect('/shop')

@app.route('/avatarshop', methods=['GET', 'POST'])
def avatarshop():
    player_id = session['player_id']
    player = Player.query.filter_by(id=player_id).first()

    if request.method == 'GET':
        shopItems = ShopItem.query.join(ShopItem.item).filter(Item.category == 'avatar').all()
        print(shopItems)
        return render_template('avatarshop.html', shopItems=shopItems, balance=player.balance)
    else:
        shop_item_id = request.form.get('itemId')
        shop_item = ShopItem.query.filter_by(id=shop_item_id).first()

        if player.balance < shop_item.price:
            return render_template('error.html', message='not enough money')

        player.balance -= shop_item.price
        player_item = PlayerItem(item=shop_item.item, player=player)
        db.session.add(player_item)
        db.session.commit()

        return redirect('/avatarshop')

@app.route('/profile')
def profile():
    player_id = session['player_id']
    player = Player.query.filter_by(id=player_id).first()
    # ShopItem.query.join(ShopItem.item).filter(Item.category == 'general').all()
    generalItems = PlayerItem.query.filter_by(player=player).join(PlayerItem.item).filter(Item.category == 'general').all()
    print(generalItems)
    avatarItems = PlayerItem.query.filter_by(player=player).join(PlayerItem.item).filter(Item.category == 'avatar').all()

    return render_template('profile.html', generalItems=generalItems, avatarItems=avatarItems, player=player)

@app.route('/avatar', methods=['POST'])
def avatar():
    player_id = session['player_id']
    player = Player.query.filter_by(id=player_id).first()

    player.current_avatar = request.json['avatarName']
    db.session.commit()

    return request.json['avatarName']


if __name__ == '__main__':
    app.run(debug=True)
