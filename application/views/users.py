from flask import request
from flask_restx import Namespace, Resource, abort

from application.database import db
from application.exceptions import ItemNotFound
from application.services.users import UsersService

users_ns = Namespace("users")


@users_ns.route("/")
class UsersViews(Resource):
    @users_ns.response(200, "OK")
    def get(self):
        return UsersService(db.session).get_all_users()


@users_ns.route("/<int:user_id>")
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self, user_id: int):
        try:
            return UsersService(db.session).get_user_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    # @check_token
    def patch(self, user_id: int):
        req_json = request.json
        if not req_json:
            abort(400, "Try again")
        if not req_json.get("id"):
            req_json["id"] = user_id
        try:
            return UsersService(db.session).update(req_json), 204
        except ItemNotFound:
            abort(404, message="User not found")


@users_ns.route("/password/<int:user_id>")
class UserPatchView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    # @check_token
    def put(self, user_id: int):
        req_json = request.json
        password_1 = req_json.get("password_1", None)
        password_2 = req_json.get("password_2", None)
        if None in [password_1, password_2]:
            abort(400, "Try again")
        if not req_json.get('id'):
            req_json["id"] = user_id
        try:
            return UsersService(db.session).update_password(req_json)
        except ItemNotFound:
            abort(404, message="User not found")
