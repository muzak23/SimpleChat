from . import socketio
from flask_socketio import emit

from flask import render_template
from flask import Blueprint

chat = Blueprint('chat', __name__)

chatHistory = []

@chat.route("/<room>")
def room(room):
    return render_template('room.html', room=room)

# @socketio.event
# def my_event(message):
#     emit('my response', {'data': 'got it!'})


def messageReceived():
    '''
    :return : return the value message Recevied
    '''
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived())
    return 'event received'

@socketio.on('message')
def handle_message(message):
    print('received message: ' + str(message))
    message = {'author': 'Logan', 'text': message}  # Temporary hard-coded username
    chatHistory.append(message)
    test_broadcast_message(message)
    return 'messageReceived'

@socketio.on('getHistory')
def handle_getHistory():
    print('received getHistory')
    return chatHistory

@socketio.on('my broadcast event', namespace='/chat')
def test_broadcast_message(message):
    emit('newMessage', message, broadcast=True)

