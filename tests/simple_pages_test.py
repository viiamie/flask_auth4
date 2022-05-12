"""This test the homepage"""

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_request_index(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_request_about(client):
    """This makes the index page"""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"about" in response.data

def test_request_error(client):
    response = client.get("/error")
    assert response.status_code == 404

def test_request_navbar(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/">welcome'
    assert b'href="/about"' in response.data