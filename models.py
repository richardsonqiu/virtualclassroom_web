from app import db
from werkzeug.security import generate_password_hash

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    room_name = db.Columen(db.String(20), nullable=False)
    player_items = db.relationship('PlayerItem', back_populates='player')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.currency = 0
        self.room_name = 'TEST'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class PlayerItem(db.Model):
    __tablename__ = 'player_item'

    id = db.Column(db.Integer, primary_key=True)
    item = db.relationship('Item', uselist=False)


class ShopItem(db.Model):
    __tablename__ = 'shop_item'

    id = db.Column(db.Integer, primary_key=True)
    item = db.relationship('Item', uselist=False)
    price = db.Column(db.Integer, nullable=False)
