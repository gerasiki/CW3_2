from sqlalchemy.orm import scoped_session

from application.dao.models.user import User
from application.tools.security import make_user_password_hash, compare_passwords


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, uid: int):
        return self._db_session.query(User).filter(User.id == uid).first()

    def get_all(self):
        return self._db_session.query(User).all()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, user_data):
        new_user = User(**user_data)
        self._db_session.add(new_user)
        self._db_session.commit()
        # return new_user

    def update(self, user_id):
        user = self.get_by_id(user_id.get("id"))
        user.email = user_id.get("email")
        user.name = user_id.get("name")
        user.surname = user_id.get("surname")
        user.favorite_genre = user_id.get("favorite_genre")

        self._db_session.add(user)
        self._db_session.commit()

    def update_password(self, user_id):
        user = self.get_by_id(user_id.get("id"))
        password_1 = user_id.get("password_1")
        if compare_passwords(user.pass_hash, password_1):
            user.password = user_id.get("password_2")
            user.pass_hash = make_user_password_hash(user.password)
        else:
            return "Не корректный пароль"

        self._db_session.add(user)
        self._db_session.commit()

    def delete(self, uid):
        user = self.get_by_id(uid)
        self._db_session.delete(user)
        self._db_session.commit()
