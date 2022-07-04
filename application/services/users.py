from application.dao.user_dao import UserDAO
from application.exceptions import ItemNotFound
from application.schemas.user import UserSchema
from application.services.base import BaseService
from application.tools.security import make_user_password_hash


class UsersService(BaseService):
    def get_user_by_id(self, uid):
        user = UserDAO(self.db_session).get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self.db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_user_by_email(self, email):
        user = UserDAO(self.db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def create_user(self, new_user):
        user_password_hash = new_user.get("password")
        if user_password_hash:
            new_user["pass_hash"] = make_user_password_hash(user_password_hash)
        user = UserDAO(self.db_session).create(new_user)
        return UserSchema(many=True).dump(user)

    def update(self, uid):
        UserDAO(self.db_session).update(uid)

    def update_password(self, req_json):
        # user_password_1 = req_json.get("password_1")
        # user_password_2 = req_json.get("password_2")
        UserDAO(self.db_session).update_password(req_json)

