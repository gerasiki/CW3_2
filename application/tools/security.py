import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app, request, abort

from application.exceptions import ItemNotFound

secret = 's3cR$eT'
algo = 'HS256'


def make_user_password_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"]
    ))


def compare_passwords(password_hash, other_password) -> bool:
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        (hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=other_password.encode("utf-8"),
            salt=current_app.config["PWD_HASH_SALT"],
            iterations=current_app.config["PWD_HASH_ITERATIONS"])))


def user_auth(req_json, user):
    user_email = req_json.get("email")
    user_password = req_json.get("password")
    if user_email and user_password:
        password_hash = user["pass_hash"]
        req_json["role"] = 'user'
        req_json["id"] = user["id"]
        if compare_passwords(password_hash, user_password):
            return create_token(req_json)
    raise ItemNotFound


def create_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algorithm=algo)
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens, 202


def refresh_token_(req_json):
    old_token = req_json.get("refresh_token")
    data = jwt.decode(old_token, secret, algorithms=[algo])
    if data:
        tokens = create_token(data)
        return tokens
    raise ItemNotFound


def check_token(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)
    return wrapper
