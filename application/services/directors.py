from application.dao.director_dao import DirectorDAO
from application.exceptions import ItemNotFound
from application.schemas.director import DirectorSchema
from application.services.base import BaseService


class DirectorsService(BaseService):
    def get_one_by_id(self, did):

        director = DirectorDAO(self.db_session).get_by_id(did)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self, condition):
        if condition.get("page") is not None:
            directors = DirectorDAO(self.db_session).get_by_page(int(condition.get("page")))
        else:
            directors = DirectorDAO(self.db_session).get_all()
        return DirectorSchema(many=True).dump(directors)
