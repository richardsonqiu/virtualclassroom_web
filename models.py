from flask_sqlalchemy import Model, SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Integer, default=0, nullable=False)
    room_name = db.Column(db.String(20), default='TEST', nullable=False)
    player_items = db.relationship('PlayerItem')
    current_avatar = db.Column(db.String, default='vBasicController_allie chibi', nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)


class PlayerItem(db.Model):
    __tablename__ = 'player_item'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(Player.id), nullable=False)
    player = db.relationship(Player, uselist=False)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id), nullable=False)
    item = db.relationship(Item, lazy="joined", innerjoin=True, uselist=False)


class ShopItem(db.Model):
    __tablename__ = 'shop_item'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id), nullable=False)
    item = db.relationship(Item, lazy="joined", innerjoin=True, uselist=False)
    price = db.Column(db.Integer, nullable=False)