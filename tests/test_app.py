import importlib
from unittest.mock import patch


def test_app_is_created(app):
    assert app is not None
    assert app.testing is True


def test_index_route(client):
    """Exemplo de teste de rota — ajuste se sua rota for diferente."""
    response = client.get("/")

    assert response.status_code in (200, 404)


def test_create_app_with_no_namespaces(monkeypatch):
    with patch("src.resource.all_namespaces", return_value=[]):
        import src.external as api

        api = importlib.reload(api)

        app = api.create_app()

        assert app is not None
        assert isinstance(app.name, str)
