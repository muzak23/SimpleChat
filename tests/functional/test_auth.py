def test_generate_random_name_endpoint(client):
    """
    GIVEN a random name generation endpoint
    WHEN the endpoint is accessed
    THEN check that a 200 status code and a single name string within length requirements is returned
    """
    response = client.get('/generateRandomName')
    assert response.status_code == 200
    name = response.get_data(as_text=True)
    assert isinstance(name, str)
    assert len(name) > 3
    assert len(name) < 32


def test_login_endpoint_valid_username(client):
    """
    GIVEN a login endpoint
    WHEN the endpoint is accessed with a valid username
    THEN check that a 200 status code is returned
    """
    response = client.post('/login', data={'username': 'testuser'})
    assert response.status_code == 200


def test_login_endpoint_empty_username(client):
    """
    GIVEN a login endpoint
    WHEN the endpoint is accessed with an empty username
    THEN check that a 200 status code and an error code of -1 is returned
    """
    response = client.post('/login', data={'username': ''})
    assert response.status_code == 200
    assert b'-1' in response.data


def test_login_endpoint_short_username(client):
    """
    GIVEN a login endpoint
    WHEN the endpoint is accessed with a username that is too short
    THEN check that a 200 status code and an error code of -1 is returned
    """
    response = client.post('/login', data={'username': 'ab'})
    assert response.status_code == 200
    assert b'-1' in response.data


def test_login_endpoint_long_username(client):
    """
    GIVEN a login endpoint
    WHEN the endpoint is accessed with a username that is too long
    THEN check that a 200 status code and an error code of -1 is returned
    """
    long_username = 'a' * 33  # 33 characters, exceeding the limit
    response = client.post('/login', data={'username': long_username})
    assert response.status_code == 200
    assert b'-1' in response.data


def test_login_endpoint_special_characters_username(client):
    """
    GIVEN a login endpoint
    WHEN the endpoint is accessed with a username containing special characters
    THEN check that a 200 status code and an error code of -1 is returned
    """
    response = client.post('/login', data={'username': 'user!@#'})
    assert response.status_code == 200
    assert b'-1' in response.data


def test_login_endpoint_duplicate_username(app, client):
    """
    GIVEN a login endpoint and an existing persistent user
    WHEN the endpoint is accessed with a duplicate username
    THEN check that a 200 status code and an error code of -2 is returned
    """
    with app.app_context():
        from simplechat.models import User
        from simplechat import db

        # Create an initial user
        user = User(username='duplicateuser', persistent=True)
        db.session.add(user)
        db.session.commit()

        # Attempt to log in with the same username
        response = client.post('/login', data={'username': 'duplicateuser'})
        assert response.status_code == 200
        assert b'-2' in response.data
