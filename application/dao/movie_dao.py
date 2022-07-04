from typing import Optional, TypeVar

import sqlalchemy.sql.expression
from flask import current_app
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from application.dao.models.movie import Movie

T = TypeVar('T', bound=Movie)


def _items_per_page() -> int:
    return current_app.config['ITEMS_PER_PAGE']


class MovieDAO:
    __model__ = Movie

    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, mid: int):
        return self._db_session.query(Movie).filter(Movie.id == mid).first()

    def get_all(self):
        return self._db_session.query(Movie).all()

    def get_by_page(self, page: Optional[int] = 1, status: Optional[str] = None):
        items_num = _items_per_page()
        try:
            if status is not None:
                desc_filter = sqlalchemy.sql.expression.desc(Movie.year)
                return self._db_session.query(Movie).order_by(desc_filter).paginate(page, items_num, False).items
            else:
                return self._db_session.query(Movie).paginate(page, items_num, False).items
        except NotFound:
            return []

    def get_by_director_id(self, did):
        return self._db_session.query(Movie).filter(Movie.director_id == did).all()

    def get_by_genre_id(self, gid):
        return self._db_session.query(Movie).filter(Movie.genre_id == gid).all()

    def get_by_year(self, year):
        return self._db_session.query(Movie).filter(Movie.year == year).all()

    def create(self, movie_id):
        new_movie = Movie(**movie_id)
        self._db_session.add(new_movie)
        self._db_session.commit()
        return new_movie

    def update(self, movie_id):
        movie = self.get_by_id(movie_id.get("id"))
        movie.title = movie_id.get("title")
        movie.description = movie_id.get("description")
        movie.trailer = movie_id.get("trailer")
        movie.year = movie_id.get("year")
        movie.rating = movie_id.get("rating")
        movie.genre_id = movie_id.get("genre_id")
        movie.director_id = movie_id.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()

    def delete(self, mid):
        movie = self.get_by_id(mid)
        self._db_session.delete(movie)
        self._db_session.commit()
