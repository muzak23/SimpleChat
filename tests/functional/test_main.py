def test_main_page(client):
    """
    GIVEN the main page endpoint
    WHEN the endpoint is accessed
    THEN check that a 200 status code is returned and the page contains 'SimpleChat'
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'SimpleChat' in response.data
