from application.app_creator import create_app
from application.config import DevelopmentConfig
# from config import config
from database import db

app = create_app(DevelopmentConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
