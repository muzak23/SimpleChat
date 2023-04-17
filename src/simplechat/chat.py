import random
import re

from . import socketio

from flask import Blueprint, request, render_template

from flask_login import login_required, logout_user, current_user, login_user

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
        return current_user
    else:
        return -1
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@socketio.on('message')
def handle_message(message_text):
    print('received message: ' + str(message_text))
    message_text = message_text.strip()
    message = Message(user_id=current_user.id, text=message_text)
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


@socketio.on('generateRandomName')
def handle_generateRandomName():
    print('Generating random name...')
    return random.choice(NAMES_ADJECTIVE) + ' ' + random.choice(NAMES_NOUN)


# @socketio.on('login')
# def handle_login(username):
#     print('Logging in user: ' + str(username))
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         user = User(username=username)
#         db.session.add(user)
#         db.session.commit()
#     login_user(user)
#     return user.id

@chat.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    print('Logging in user: ' + str(username))
    username = username.strip()
    username = re.sub(' {2,}', ' ', username)
    if username == '' or re.match('[a-zA-Z ]+$', username) is None or 3 > len(username) > 21:
        return '-1'  # Invalid username
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print('Created new user: ' + str(user))
        return '1'  # User created
    else:
        return '-2'  # User already exists
