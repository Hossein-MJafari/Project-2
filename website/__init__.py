from flask import *
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret key"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = '\\website\\static'

    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Product
    create_database(app)

    return app


def create_database(app):
    if not os.path.exists('instance/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")
