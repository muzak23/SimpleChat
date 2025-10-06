import random
import re

from flask import Blueprint, request

from flask_login import login_user

from . import db
from .models import User


auth = Blueprint('auth', __name__)


NAMES_ADJECTIVE = ['Adorable', 'Beautiful', 'Charming', 'Dazzling', 'Elegant', 'Fancy', 'Glamorous', 'Handsome',
                   'Magnificent', 'Sparkling', 'Aggressive', 'Agreeable', 'Ambitious', 'Brave', 'Calm', 'Delightful',
                   'Eager', 'Faithful', 'Gentle', 'Happy', 'Jolly', 'Kind', 'Lively', 'Nice', 'Obedient', 'Polite',
                   'Proud', 'Silly', 'Thankful', 'Victorious', 'Witty', 'Wise', 'Zealous', 'Bashful'
                   ]
NAMES_NOUN = ['Lynx', 'Octopus', 'Duck', 'Platypus', 'Toad', 'Squirrel', 'Deer', 'Rabbit', 'Hedgehog', 'Pig', 'Cat',
              'Dog', 'Lion', 'Tiger', 'Bear', 'Wolf', 'Fox', 'Panda', 'Koala', 'Giraffe', 'Elephant', 'Rhino', 'Hippo',
              'Zebra', 'Horse', 'Cow', 'Sheep', 'Goat', 'Chicken', 'Penguin', 'Owl', 'Frog', 'Snake', 'Lizard',
              'Turtle', 'Fish', 'Shark', 'Whale', 'Dolphin', 'Seal', 'Otter', 'Monkey', 'Gorilla', 'Kangaroo',
              'Raccoon', 'Mouse', 'Rat', 'Beaver', 'Sloth', 'Polar Bear'
              ]


@auth.route('/generateRandomName', methods=['GET'])
def handle_generate_random_name():
    return random.choice(NAMES_ADJECTIVE) + ' ' + random.choice(NAMES_NOUN)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    username = username.strip()
    username = re.sub(' {2,}', ' ', username)
    if username == '' or re.match('[a-zA-Z0-9 ]+$', username) is None or not 3 < len(username) < 32:
        return '-1'  # Invalid username
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print('Created new user: ' + str(user))
        return '1'  # User created
    elif not user.persistent:
        login_user(user)
        print('Logged in user: ' + str(user))
        return '0'  # User logged in
    else:
        return '-2'  # User already exists
