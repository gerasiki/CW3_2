from application.dao.movie_dao import MovieDAO
from application.exceptions import ItemNotFound
from application.schemas.movie import MovieSchema
from application.services.base import BaseService


class MoviesService(BaseService):
    # def __init__(self, dao: MovieDAO):
    #     self.dao = dao

    def get_one_by_id(self, mid):
        movie = MovieDAO(self.db_session).get_by_id(mid)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, condition):
        if condition.get("director_id") is not None:
            movies = MovieDAO(self.db_session).get_by_director_id(condition.get("director_id"))
        elif condition.get("genre_id") is not None:
            movies = MovieDAO(self.db_session).get_by_genre_id(condition.get("genre_id"))
        elif condition.get("year") is not None:
            movies = MovieDAO(self.db_session).get_by_year(condition.get("year"))
        elif condition.get("page") is not None:
            movies = MovieDAO(self.db_session).get_by_page(int(condition.get("page")), condition.get("status"))
        else:
            movies = MovieDAO(self.db_session).get_all()
        return MovieSchema(many=True).dump(movies)

    def create(self, mid):
        MovieDAO(self.db_session).create(mid)
        # return MovieSchema().dump(movie)

    def update(self, mid):
        MovieDAO(self.db_session).update(mid)
        # return MovieSchema().dump(movie)

    def delete(self, mid):
        MovieDAO(self.db_session).delete(mid)
