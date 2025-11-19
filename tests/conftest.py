import os
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Row, create_engine
from sqlalchemy.orm import sessionmaker

from src.db.database import db
from src.external import create_app
from src.model.groups import Client


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Define variáveis de ambiente específicas para testes."""
    os.environ["FLASK_ENV"] = "testing"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    db.Model.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def session(engine):
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def app():
    """
    Cria uma instância do app Flask para testes.
    Aqui o verify_database_connection é totalmente mockado.
    """

    with patch("src.db.extensions.verify_database_connection") as mock_verify:
        mock_verify.return_value = True

        app = create_app()
        app.testing = True

        # Remove o middleware real nos testes
        app.wsgi_app = app.wsgi_app

        yield app


@pytest.fixture
def client(app):
    """Client de testes do Flask."""
    return app.test_client()


@pytest.fixture
def fake_app():
    """Mocka um app Flask apenas para testar o app_context()."""
    app = MagicMock()
    app.app_context.return_value.__enter__.return_value = None
    app.app_context.return_value.__exit__.return_value = None
    return app


@pytest.fixture
def sample_client():
    """Fixture for a sample Client instance."""
    return Client(
        name="João Silva",
        email="joao@email.com",
        cpf_cnpj="123.456.789-00",
    )


@pytest.fixture
def sample_clients():
    """Fixture for a list of sample Client instances."""
    return [
        Client(
            name="João Silva",
            email="joao1@email.com",
            cpf_cnpj="123.456.789-00",
        ),
        Client(
            name="Maria Santos",
            email="maria@email.com",
            cpf_cnpj="987.654.321-00",
        ),
    ]


@pytest.fixture
def mock_row():
    """Mock SQLAlchemy Row object."""
    mapping_dict = {"id": 1, "name": "João", "email": "joao@email.com"}
    row = MagicMock(spec=Row)
    row._mapping = mapping_dict  # Use real dict for _mapping
    return row


@pytest.fixture
def mock_model():
    """Mock model instance with __table__."""
    mock = MagicMock()
    mock.__table__ = MagicMock()
    mock.__table__.columns = [MagicMock(name="id"), MagicMock(name="name")]
    mock.id = 1
    mock.name = "Test"
    return mock
