from app.db.models import Movies, db, User
from flask_login import FlaskLoginClient
import pytest


def test_browse_movies(client):
    assert client.post("login", data={"email": "email@email.com", "password": "!Testtest1", "confirm": "!Testtest1"})
    assert client.get("/login").status_code == 200

def test_add_movie(application):
    with application.app_context():
        assert db.session.query(Movies).count() == 0
        movie = Movies("title", "descrip", "rating", "1")
        db.session.add(movie)
        movie = Movies.query.filter_by(title="title").first()
        assert movie.title == "title"

def test_edit_movie(application):
    application.test_client_class = FlaskLoginClient
    user = User('email@email', '!Testtest1')
    movie = Movies("title", "description", "rating", "1")
    db.session.add(user)
    db.session.add(movie)
    db.session.commit()

    assert db.session.query(User).count() == 1
    assert db.session.query(Movies).count() == 1

    with application.test_client(user=user) as client:
        response = client.post('/movies/edit/1',
                               data={"title": "testTitle", "description": "testDescrip", "rating": "testRating"},
                               follow_redirects=True)

def test_delete_movie(application):
    application.test_client_class = FlaskLoginClient
    user = User('email@email.com', '!Testtest1')
    movie = Movies("title", "description", "rating", "1")
    db.session.add(user)
    db.session.add(movie)
    db.session.commit()

    assert user.email == 'email@email.com'
    assert db.session.query(User).count() == 1
    assert db.session.query(Movies).count() == 1

    with application.test_client(user=user) as client:
        response = client.get('/movies/delete/1', follow_redirects=True)