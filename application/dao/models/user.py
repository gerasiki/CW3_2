from application.database import db
from application.dao.models.base_model import Base


class User(Base, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(90), unique=True, nullable=False)
    pass_hash = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String(255))
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.String)

    def __repr__(self):
        return f"<User '{self.name.title()}'>"
