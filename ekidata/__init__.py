from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from ekidata.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from ekidata.seed import bp as seed_bp
    app.register_blueprint(seed_bp)

    return app

from ekidata import models
