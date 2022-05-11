from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class addMovieForm(FlaskForm):
    movie_title = StringField('Title', [validators.DataRequired()], description="Title of the movie")
    movie_description = TextAreaField('Movie Description', [validators.DataRequired()], description="Movie description goes here")
    submit = SubmitField()

class editMovieForm(FlaskForm):
    movie_title = StringField('Title', [validators.DataRequired()], description="Title of the movie")
    movie_description = TextAreaField('Movie Description', [validators.DataRequired()], description="Movie description goes here")
    submit = SubmitField()