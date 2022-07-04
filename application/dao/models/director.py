from application.database import db
from application.dao.models.base_model import Base


class Director(Base, db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Director '{self.name.title()}'>"
