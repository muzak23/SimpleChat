import re
from datetime import datetime

from . import socketio

from flask import Blueprint, render_template

from flask_login import logout_user, current_user
from flask_socketio import emit, join_room

from . import db, login_manager
from .models import User, Message, Room

chat = Blueprint('chat', __name__)


@chat.route("/<room>")
def room(room):
    if len(room) > 32 or not re.match(r'^[A-Za-z0-9_-]+$', room):
        return render_template('bad_request.html'), 400
    return render_template('room.html', room=room)


@socketio.on('connect')
def connect_handler():
    print(f'{current_user} is trying to connect')
    if current_user.is_authenticated:
        data = {'id': current_user.id, 'username': current_user.username}
        emit('connected', data)
        return current_user
    else:
        print('user is not authenticated')
        emit('disconnect', 'notAuthenticated')


# @socketio.on('reconnect')
# def reconnect_handler():
#     print(f'{current_user} is trying to reconnect')
#     if current_user.is_authenticated:
#         data = {'id': current_user.id, 'username': current_user.username}
#         socketio.emit('reconnected', data)
#         return current_user
#     else:
#         socketio.emit('disconnect')


@socketio.on('join')
def on_join(room):
    print('User ' + current_user.username + ' has entered the room ' + room + '.')
    join_room(room)
#     socketio.emit(username + ' has entered the room.', room=room)
#


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@socketio.on('message')
def handle_message(message_data):
    message_text = message_data['message']
    room_text = message_data['room']
    print('received message: ' + str(message_text))
    if current_user.is_authenticated is False:
        print('user is not authenticated')
        # socketio.emit('notAuthenticated')
        return 'notAuthenticated'
    if message_text is None or str(message_text).isspace() or message_text == ''\
            or len(message_text) > 2048 or len(room_text) > 32:
        print('message is invalid')
        return 'invalidMessage'
    message_text = message_text.strip()
    room_obj = Room.query.filter_by(name=room_text).first()
    if room_obj is None:
        room_obj = Room(name=room_text)
        db.session.add(room_obj)
        db.session.commit()
    message = Message(user_id=current_user.id, room_id=room_obj.id, text=message_text)
    db.session.add(message)
    db.session.commit()
    print('responding with ' + str(message.to_dict()))
    socketio.emit('newMessage', message.to_dict(), include_self=False, to=room_text)
    print('emitted newMessage')
    return 'messageReceived'


@socketio.on('getHistory')
def handle_get_history(room, before=None, after=None):
    print('getting history')
    room_obj = Room.query.filter_by(name=room).first()
    if room_obj is None:
        return []
    if before:
        print('before' + str(before))
        before = datetime.fromtimestamp(int(before))
        chat_history = (Message.query
                        .filter(Message.room_id == room_obj.id)
                        .filter(Message.timestamp < before)
                        .order_by(Message.timestamp.desc())
                        .limit(20).all())
    elif after:
        print('after' + str(after))
        chat_history = (Message.query
                        .filter(Message.room_id == room_obj.id)
                        .filter(Message.timestamp > after)
                        .order_by(Message.timestamp.desc())
                        .limit(20).all())
    else:
        print('else')
        chat_history = (Message.query
                        .filter(Message.room_id == room_obj.id)
                        .order_by(Message.timestamp.desc())
                        .limit(20).all())
    chat_history = [message.to_dict() for message in chat_history]
    print(chat_history)
    return chat_history


@socketio.on('getUsername')
def handle_get_user(id):
    return str(User.query.get(id).username)


@socketio.on('newUser')
def handle_new_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user.id


@socketio.on('logout')
def handle_logout():
    logout_user()
    return 'Logged out'
