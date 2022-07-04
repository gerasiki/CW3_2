from flask import request
from flask_restx import Namespace, Resource, abort

from application.database import db
from application.exceptions import ItemNotFound
from application.services.movies import MoviesService

movies_ns = Namespace("movies")


@movies_ns.route('/')
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    def get(self):
        director = request.args.get('director_id')
        genre = request.args.get('genre_id')
        year = request.args.get('year')
        status = request.args.get('status')
        page = request.args.get('page')
        condition = {
            'director_id': director,
            'genre_id': genre,
            'year': year,
            'status': status,
            'page': page
        }
        return MoviesService(db.session).get_all_movies(condition)


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, movie_id: int):
        try:
            return MoviesService(db.session).get_one_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")
