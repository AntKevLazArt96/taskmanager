import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    """Crea la aplicación en modo prueba"""
    app = create_app()

    # Configurar para usar BD en memoria
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Desactiva CSRF para las pruebas

    return app


@pytest.fixture
def client(app):
    """Cliente para simular peticiones HTTP"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Para ejecutar comandos CLI (opcional, pero útil)"""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Base de datos limpia para cada prueba"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()