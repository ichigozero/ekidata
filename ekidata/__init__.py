from flask import Flask
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)

    from ekidata.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/ekidata/api')

    from ekidata.seed import bp as seed_bp
    app.register_blueprint(seed_bp)

    from ekidata.seed_mongo import bp as seed_mongo_bp
    app.register_blueprint(seed_mongo_bp)

    app.register_error_handler(404, not_found)

    return app

from ekidata import models

def not_found(error):
    return {'error': 'Not found'}, 404
