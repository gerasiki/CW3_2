from application.app_creator import create_app
from application.config import DevelopmentConfig
from application.dao.models.director import Director
from application.dao.models.genre import Genre
from application.dao.models.movie import Movie
from application.dao.models.user import User
from application.database import db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User
    }


if __name__ == '__main__':
    app.run()
