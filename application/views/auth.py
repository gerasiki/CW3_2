from flask import request
from flask_restx import Namespace, Resource, abort

from application.database import db
from application.exceptions import ItemNotFound
from application.services.users import UsersService
from application.tools.security import user_auth, refresh_token_

login_ns = Namespace("login")
register_ns = Namespace('register')


@login_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)
        if None in [email, password]:
            abort(400)
        try:
            user = UsersService(db.session).get_user_by_email(email=email)
            tokens = user_auth(req_json, user)
            return tokens, 201
        except ItemNotFound:
            abort(401, "Authorisation's error")

    def put(self):
        req_json = request.json
        if None in req_json:
            abort(400)
        try:
            tokens = refresh_token_(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, "Authorisation's error")


@register_ns.route('/')
class AuthRegView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")
        return UsersService(db.session).create_user(req_json)
