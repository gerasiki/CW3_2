from flask import request
from flask_restx import Namespace, Resource, abort

from application.database import db
from application.exceptions import ItemNotFound
from application.services.genres import GenresService

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.response(200, "OK")
    def get(self):
        page = request.args.get('page')
        condition = {'page': page}
        return GenresService(db.session).get_all_genres(condition)


@genres_ns.route("/<int:genre_id>")
class GenreView(Resource):
    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    def get(self, genre_id: int):
        try:
            return GenresService(db.session).get_one_by_id(genre_id)
        except ItemNotFound:
            abort(404, message="Genre not found")
