from flask import Blueprint, render_template, flash, url_for, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect

from app.auth import admin_required
from app.db import db
from app.db.models import Movies
from app.movie.forms import addMovieForm, editMovieForm

movie = Blueprint('movie', __name__, template_folder='templates')


@movie.route('/movies', methods=['GET'], defaults={"page": 1})
@movie.route('/movies/<int:page>', methods=['GET'])
@login_required
def browse_movies(page):
    page = page
    per_page = 10
    pagination = Movies.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'User ID')]
    retrieve_url = ('movie.retrieve_movie', [('movie_id', ':id')])
    return render_template('browse_movies.html', titles=titles, data=data, retrieve_url=retrieve_url, Movies=Movies)


@movie.route('/movies/view/<int:movie_id>', methods=['GET'])
@login_required
def retrieve_movie(movie_id):
    movies = Movies.query.get(movie_id)
    return render_template('view_movie.html', movies=movies)


@movie.route('/movies/add', methods=['POST', 'GET'])
@login_required
def add_movie():
    add_movie_form = addMovieForm()
    if add_movie_form.validate_on_submit():
        movies = Movies(title=add_movie_form.movie_title.data, content=add_movie_form.movie_description.data,
                        rating=add_movie_form.movie_rating.data, user_id=current_user.id)
        db.session.add(movies)
        db.session.commit()
        flash("New movie added successfully", "success")
        return redirect(url_for('movie.my_movies'))
    try:
        return render_template('add_movie.html', form=add_movie_form)
    except TemplateNotFound:
        abort(404)


@movie.route('/movies/edit/<int:movie_id>', methods=['POST', 'GET'])
@login_required
def edit_movie(movie_id):
    movies = Movies.query.get(movie_id)
    if current_user.id != movies.user_id and current_user.is_admin is False:
        flash("You cannot edit this movie")
        return redirect(url_for('movie.my_movies'))

    edit_movie_form = editMovieForm(obj=movies)
    if edit_movie_form.validate_on_submit():
        db.session.delete(movies)
        movies = Movies(title=edit_movie_form.movie_title.data, content=edit_movie_form.movie_description.data,
                        rating=edit_movie_form.movie_rating.data, user_id=current_user.id)
        db.session.add(movies)
        db.session.commit()
        flash("Movie edited successfully", "success")
        return redirect(url_for('movie.my_movies'))
    return render_template('edit_movie.html', form=edit_movie_form)


@movie.route('/movies/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    movies = Movies.query.get(movie_id)
    if current_user.id == movies.user_id or current_user.is_admin:
        db.session.delete(movies)
        db.session.commit()
        flash('Movie deleted', 'success')
    else:
        flash("You can not delete this movie")
    return redirect(url_for('movie.my_movies'))


@movie.route('/movies/my', methods=['GET'], defaults={"page": 1})
@movie.route('/movies/my/<int:page>', methods=['GET'])
@login_required
def my_movies(page):
    page = page
    per_page = 10
    pagination = Movies.query.filter(Movies.user_id == current_user.id).paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'User ID')]
    retrieve_url = ('movie.retrieve_movie', [('movie_id', ':id')])
    edit_url = ('movie.edit_movie', [('movie_id', ':id')])
    add_url = url_for('movie.add_movie')
    delete_url = ('movie.delete_movie', [('movie_id', ':id')])
    return render_template('browse_movies.html', titles=titles, data=data, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, retrieve_url=retrieve_url, Movies=Movies)


@movie.route('/movies/admin', methods=['GET'], defaults={"page":1})
@movie.route('/movies/admin/<int:page>', methods=['GET'])
@login_required
@admin_required
def manage_movies(page):
    page = page
    per_page = 10
    pagination = Movies.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'User ID')]
    retrieve_url = ('movie.retrieve_movie', [('movie_id', ':id')])
    edit_url = ('movie.edit_movie', [('movie_id', ':id')])
    add_url = url_for('movie.add_movie')
    delete_url = ('movie.delete_movie', [('movie_id', ':id')])
    return render_template('browse_movies.html', titles=titles, data=data, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, retrieve_url=retrieve_url, Movies=Movies)