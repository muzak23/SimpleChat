from . import db

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    persistent = db.Column(db.Boolean, default=False)
    # email = db.Column(db.String(120), index=True, unique=True)  # Not implemented yet
    # password_hash = db.Column(db.String(128))  # Not implemented yet
    # salt = db.Column(db.String(32))  # Not implemented yet

    messages = db.relationship('Message', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'id={self.id},username={self.username}'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    text = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'id={self.id},user_id={self.user_id},room_id={self.room_id},text={self.text},timestamp={self.timestamp}'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.author.username,
            'room_id': self.room_id,
            'text': self.text,
            'timestamp': int(self.timestamp.replace(tzinfo=timezone.utc).timestamp())
        }


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    messages = db.relationship('Message', backref='room', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'
