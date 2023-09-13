from . import socketio

from flask import Blueprint, render_template

from flask_login import login_required, logout_user, current_user, login_user
from flask_socketio import join_room, leave_room

from . import db, login_manager
from .models import User, Message

chat = Blueprint('chat', __name__)

NAMES_ADJECTIVE = ['Adorable', 'Beautiful', 'Charming', 'Dazzling', 'Elegant', 'Fancy', 'Glamorous', 'Handsome', 'Magnificent', 'Sparkling', 'Aggressive', 'Agreeable', 'Ambitious', 'Brave', 'Calm', 'Delightful', 'Eager', 'Faithful', 'Gentle', 'Happy', 'Jolly', 'Kind', 'Lively', 'Nice', 'Obedient', 'Polite', 'Proud', 'Silly', 'Thankful', 'Victorious', 'Witty', 'Wise', 'Zealous', 'Bashful']
NAMES_NOUN = ['Lynx', 'Octopus', 'Duck', 'Platypus', 'Toad', 'Squirrel', 'Deer', 'Rabbit', 'Hedgehog', 'Pig', 'Cat', 'Dog', 'Lion', 'Tiger', 'Bear', 'Wolf', 'Fox', 'Panda', 'Koala', 'Giraffe', 'Elephant', 'Rhino', 'Hippo', 'Zebra', 'Horse', 'Cow', 'Sheep', 'Goat', 'Chicken', 'Duck', 'Penguin', 'Owl', 'Frog', 'Snake', 'Lizard', 'Turtle', 'Fish', 'Shark', 'Whale', 'Dolphin', 'Seal', 'Otter', 'Monkey', 'Gorilla', 'Kangaroo', 'Raccoon', 'Mouse', 'Rat', 'Beaver', 'Sloth', 'Polar Bear', 'Panda', 'Koala', 'Giraffe', 'Elephant', 'Rhino', 'Hippo', 'Zebra', 'Horse', 'Cow', 'Sheep', 'Goat', 'Chicken', 'Duck', 'Penguin', 'Owl', 'Frog', 'Snake', 'Lizard', 'Turtle', 'Fish', 'Shark', 'Whale', 'Dolphin', 'Seal', 'Otter', 'Monkey', 'Gorilla', 'Kangaroo', 'Raccoon', 'Mouse', 'Rat', 'Beaver', 'Sloth', 'Polar Bear']


@chat.route("/<room>")
def room(room):
    return render_template('room.html', room=room)


@socketio.on('connect')
def connect_handler():
    print(f'{current_user} is trying to connect')
    if current_user.is_authenticated:
        data = {'id': current_user.id, 'username': current_user.username}
        socketio.emit('connected', data)
        return current_user
    else:
        print('user is not authenticated')
        # socketio.emit('notAuthenticated')
        socketio.emit('disconnect', 'notAuthenticated')
        # socketio.disconnect()

# @socketio.on('reconnect')
# def reconnect_handler():
#     print(f'{current_user} is trying to reconnect')
#     if current_user.is_authenticated:
#         data = {'id': current_user.id, 'username': current_user.username}
#         socketio.emit('reconnected', data)
#         return current_user
#     else:
#         socketio.emit('disconnect')

# @socketio.on('join')
# def on_join(room):
#     print('User ' + current_user.username + ' has entered the room ' + room + '.')
#     username = current_user.username
#     join_room(room)
#     socketio.emit(username + ' has entered the room.', room=room)
#

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@socketio.on('message')
def handle_message(message_text):
    print('received message: ' + str(message_text))
    if current_user.is_authenticated is False:
        print('user is not authenticated')
        # socketio.emit('notAuthenticated')
        return 'notAuthenticated'
    if message_text is None or str(message_text).isspace() or message_text == ''\
            or len(message_text) > 1000:
        print('message is invalid')
        return 'invalidMessage'
    message_text = message_text.strip()
    message = Message(user_id=current_user.id, text=message_text)
    db.session.add(message)
    db.session.commit()
    print('responding with ' + str(message.to_dict()))
    socketio.emit('newMessage', message.to_dict(), include_self=False)
    print('emitted newMessage')
    return 'messageReceived'



@socketio.on('getHistory')
def handle_getHistory(before=None, after=None):
    if before:
        chat_history = Message.query.filter(Message.timestamp < before).order_by(Message.timestamp.desc()).limit(20).all()
    elif after:
        chat_history = Message.query.filter(Message.timestamp > after).order_by(Message.timestamp.desc()).limit(20).all()
    else:
        chat_history = Message.query.order_by(Message.timestamp.desc()).limit(20).all()
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


@socketio.on('logout')
def handle_logout():
    logout_user()
    return 'Logged out'
