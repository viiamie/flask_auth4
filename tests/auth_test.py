"""This tests the homepage"""

import pytest
from flask import session
from app.db.models import User

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/movies")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_success(client):
    """This tests for successful registration"""
    assert client.get("register").status_code == 200
    # successful registration redirects to the login page
    response = client.post("register", data={"email": "email@email.com", "password": "Testtest1!",
                                             "confirm": "Testtest1!"})
    # checks if user is inserted in database
    with client.application.app_context():
        assert User.query.filter_by(email="email@email.com").first() is not None
    assert "/login" == response.headers["Location"]

def test_logout_success(client):
    """This tests that the user logged out successfully"""
    client.post("/login", data={"email": "email@email.com", "password": "Testtest1!"}, follow_redirects=True)
    with client:
        client.get("/logout")
        assert "_user_id" not in session

def test_register_badPassword_matching(client):
    """This tests a bad password that does not match (registration)"""
    response = client.post("/register", data={"email": "test@email.com", "password": "Testtest1!",
                                              "confirm": "Testtest2!"}, follow_redirects=True)
    assert b"Passwords must match" in response.data

@pytest.mark.parametrize(
    ("email", "password", "confirm"),
    (("test@email.com", "abc", "abc"),
    ("test@email.com", "1", "1")),
)

def test_register_badPassword_criteria(client, email, password, confirm):
    """This tests a bad password that does not meet the criteria (registration)"""
    response = client.post("/register", data=dict(email=email, password=password, confirm=confirm),
                           follow_redirects=True)
    assert response.status_code == 200

def test_register_badEmail(client):
    """This tests an invalid email being used for registration"""
    response = client.post("/register", data={"email": "", "password": "Testtest1!", "confirm": "Testtest1!"}, follow_redirects=True)
    assert response.status_code == 200

def test_login_badEmail(client):
    """This tests logging in with invalid email"""
    response = client.post("/login", data={"email": "e", "password": "Testtest0!", "confirm": "Testtest0!"}, follow_redirects=True)
    assert b"Invalid username or password" in response.data

def test_login_badPassword(client):
    """This tests logging in with invalid password"""
    response = client.post("/login", data={"email": "email@email.com", "password": "wrongPassword"}, follow_redirects=True)
    assert b"Invalid username or password" in response.data

def test_already_registered(client):
    """This tests if the user is already registered"""
    with client:
        assert client.get("register").status_code == 200
        response = client.post("register", data={"email": "email@email.com", "password": "Testtest1!",
                                                 "confirm": "Testtest1!"})
        assert "/login" == response.headers["Location"]

def test_deny_movies_access(client):
    """This test denies access to the movies dashboard for users not logged-in"""
    response = client.get("/movies")
    assert "/login?next=%2Fmovies" in response.headers["Location"]
    with client:
        response = client.get("/login")
        assert b"Please log in to access this page." in response.data