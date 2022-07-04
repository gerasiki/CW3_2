from application.dao.genre_dao import GenreDAO
from application.exceptions import ItemNotFound
from application.schemas.genre import GenreSchema
from application.services.base import BaseService


class GenresService(BaseService):
    def get_one_by_id(self, gid):
        genre = GenreDAO(self.db_session).get_by_id(gid)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self, condition):
        if condition.get("page") is not None:
            directors = GenreDAO(self.db_session).get_by_page(int(condition.get("page")))
        else:
            directors = GenreDAO(self.db_session).get_all()
        return GenreSchema(many=True).dump(directors)
