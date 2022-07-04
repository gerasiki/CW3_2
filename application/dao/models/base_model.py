from application.database import db


class Base(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
