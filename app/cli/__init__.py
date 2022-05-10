import os
import click
from flask.cli import with_appcontext
from app.db import db


@click.command(name='create-db')
@with_appcontext
def create_database():
    root = os.path.dirname(os.path.abspath(__file__))
    dbdir = os.path.join(root, '../../database')
    if not os.path.exists(dbdir):
        os.mkdir(dbdir)
    db.create_all()