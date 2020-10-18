from flask_sqlalchemy import Model, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    player_classrooms = db.relationship('PlayerClassroom')

    balance = db.Column(db.Integer, default=5000, nullable=False)
    # room_name = db.Column(db.String(20), default='TEST', nullable=False)
    player_items = db.relationship('PlayerItem')
    current_avatar = db.Column(db.String, default='av_allie', nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_roomnames(self):
        return [player_classroom.classroom.roomname for player_classroom in self.player_classrooms]

    def __repr__(self):
        return '<User %r>' % self.username


class Classroom(db.Model):
    __tablename__ = 'classroom'

    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String, nullable=False)


class PlayerClassroom(db.Model):
    __tablename__ = 'player_classroom'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey(Player.id), nullable=False)
    player = db.relationship(Player, uselist=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey(Classroom.id), nullable=False)
    classroom = db.relationship(Classroom, lazy="joined", innerjoin=True, uselist=False)


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
