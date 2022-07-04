from flask import request
from flask_restx import Namespace, Resource, abort

from application.database import db
from application.exceptions import ItemNotFound
from application.services.directors import DirectorsService

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.response(200, "OK")
    def get(self):
        page = request.args.get('page')
        condition = {'page': page}
        return DirectorsService(db.session).get_all_directors(condition)


@directors_ns.route("/<int:director_id>")
class DirectorView(Resource):
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    def get(self, director_id: int):
        try:
            return DirectorsService(db.session).get_one_by_id(director_id)
        except ItemNotFound:
            abort(404, message="Director not found")
