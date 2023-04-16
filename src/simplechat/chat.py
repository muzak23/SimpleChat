from . import socketio

from flask import render_template
from flask import Blueprint

from . import db
from .models import User, Message

chat = Blueprint('chat', __name__)


@chat.route("/<room>")
def room(room):
    return render_template('room.html', room=room)


@socketio.on('message')
def handle_message(message_text):
    print('received message: ' + str(message_text))
    message = Message(user_id=1, text=message_text)  # Temporary hard-coded username
    db.session.add(message)
    db.session.commit()
    socketio.emit('newMessage', message.to_dict(), broadcast=True)
    return 'messageReceived'


@socketio.on('getHistory')
def handle_getHistory(before=None):
    if before is None:
        chat_history = Message.query.order_by(Message.timestamp.desc()).limit(20).all()
    else:
        chat_history = Message.query.filter(Message.timestamp < before).order_by(Message.timestamp.desc()).limit(20).all()
    print(chat_history)
    chat_history = [message.to_dict() for message in chat_history]
    print(chat_history)
    return chat_history


@socketio.on('getUsername')
def handle_getUser(id):
    return str(User.query.get(id).username)


@socketio.on('newUser')
def handle_newUser(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user.id

