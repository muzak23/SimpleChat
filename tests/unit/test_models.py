from simplechat.models import User, Room, Message


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username and persistent fields are defined correctly
    :return:
    """
    user = User(username='test', persistent=False)
    assert user.username == 'test'
    assert user.persistent is False


def test_new_room():
    """
    GIVEN a Room model
    WHEN a new Room is created
    THEN check the name field is defined correctly
    :return:
    """
    room = Room(name='testroom')
    assert room.name == 'testroom'


def test_new_message():
    """
    GIVEN a Message model, a User model, and a Room model
    WHEN a new Message is created
    THEN check the text, author, and room fields are defined correctly
    :return:
    """
    test_user = User(username='testuser')
    test_room = Room(name='testroom')
    message = Message(text='Hello, World!', author=test_user, room=test_room)
    assert message.text == 'Hello, World!'
    assert message.author == test_user
    assert message.room == test_room
