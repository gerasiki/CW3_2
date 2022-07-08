import os

from flask import Flask, jsonify, render_template
from flask_restx import Api

from application.database import db
from application.exceptions import BaseServiceError
from application.views.auth import auth_ns
from application.views.directors import directors_ns
from application.views.genres import genres_ns
from application.views.movies import movies_ns
from application.views.users import users_ns

api = Api(title='Course Work 3', doc='/docs')

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "application/static/templates")


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_obj):
    app = Flask(__name__, template_folder=TEMPLATE_PATH)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return render_template('index.html')

    db.init_app(app)
    api.init_app(app)

    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    # app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app
