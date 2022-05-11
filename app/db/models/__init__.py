from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    movies = db.relationship("Movies", back_populates="users", cascade="all, delete")

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    content = db.Column(db.Text, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship("User", back_populates="movies", uselist=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title