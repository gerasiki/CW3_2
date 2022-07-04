from typing import Optional

from flask import current_app
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from application.dao.models.genre import Genre


def _items_per_page() -> int:
    return current_app.config['ITEMS_PER_PAGE']


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, gid: int):
        return self._db_session.query(Genre).filter(Genre.id == gid).first()

    def get_all(self):
        return self._db_session.query(Genre).all()

    def get_by_page(self, page: Optional[int] = 1):
        items_num = _items_per_page()
        try:
            return self._db_session.query(Genre).paginate(page, items_num, False).items
        except NotFound:
            return []
