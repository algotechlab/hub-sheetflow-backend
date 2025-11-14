import os
from unittest.mock import MagicMock, patch

import pytest

from src.external import create_app


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Define variáveis de ambiente específicas para testes."""
    os.environ["FLASK_ENV"] = "testing"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"


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
