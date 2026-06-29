from flask import Flask

from .config import Config
from .extensions import csrf, db
from .routes.main import main_bp
from .routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()

    return app