import csv
import urllib.request
import json
import os
from flask import Blueprint, render_template

movie = Blueprint('movie', __name__, template_folder='templates')

@movie.route("/movies", methods=["POST","GET"], endpoint="/movies")
def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?api_key={}".format(os.environ.get("TMDB_API_KEY"))

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template("movies.html", movies=dict["results"])


@movie.route("/movies", methods=["POST","GET"])
def get_movies_list():
    url = "https://api.themoviedb.org/3/discover/movie?api_key={}".format(os.environ.get("TMDB_API_KEY"))

    response = urllib.request.urlopen(url)
    movies = response.read()
    dict = json.loads(movies)

    movies = []

    for movie1 in dict["results"]:
        movie1 = {
            "title": movie1["title"],
            "overview": movie1["overview"],
        }

        movies.append(movie1)

    return {"results": movies}
