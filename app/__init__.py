from flask import Flask

from .config import Config
from .extensions import db, csrf
from .routes.main import main_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(main_bp)

    return app