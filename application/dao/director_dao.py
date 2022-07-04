from typing import Optional

from flask import current_app
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from application.dao.models.director import Director


def _items_per_page() -> int:
    return current_app.config['ITEMS_PER_PAGE']


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, did: int):
        return self._db_session.query(Director).filter(Director.id == did).first()

    def get_all(self):
        return self._db_session.query(Director).all()

    def get_by_page(self, page: Optional[int] = 1):
        items_num = _items_per_page()
        try:
            return self._db_session.query(Director).paginate(page, items_num, False).items
        except NotFound:
            return []
