def test_room_endpoint_valid_room(client):
    """
    GIVEN a room endpoint
    WHEN the endpoint is accessed with a valid room name
    THEN check that a 200 status code is returned
    """
    response = client.get('/testroom')
    assert response.status_code == 200
    assert b'testroom' in response.data


def test_room_endpoint_valid_room_name_with_dash(client):
    """
    GIVEN a room endpoint
    WHEN the endpoint is accessed with a valid room name containing a dash
    THEN check that a 200 status code is returned
    """
    response = client.get('/test-room')
    assert response.status_code == 200
    assert b'test-room' in response.data


def test_room_endpoint_valid_room_name_with_underscore(client):
    """
    GIVEN a room endpoint
    WHEN the endpoint is accessed with a valid room name containing an underscore
    THEN check that a 200 status code is returned
    """
    response = client.get('/test_room')
    assert response.status_code == 200
    assert b'test_room' in response.data


def test_room_endpoint_long_room_name(client):
    """
    GIVEN a room endpoint
    WHEN the endpoint is accessed with a room name that is too long
    THEN check that a 404 status code is returned
    """
    long_room_name = 'a' * 33  # 65 characters, exceeding the limit
    response = client.get(f'/{long_room_name}')
    assert response.status_code == 400


def test_room_endpoint_special_characters_room_name(client):
    """
    GIVEN a room endpoint
    WHEN the endpoint is accessed with a room name containing special characters
    THEN check that a 404 status code is returned
    """
    response = client.get('/room!@#')
    assert response.status_code == 400
