from library import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_route(client):
    response = client.get('/test')
    assert response.data == b'Your app is work'