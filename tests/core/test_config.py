import importlib
import os
from unittest.mock import patch

import pytest

from src.core.config import Config, DevelopmentConfig, config_by_name


def test_default_config_values():
    """Deve carregar valores default corretamente da classe base Config"""
    with patch.dict(os.environ, {}, clear=True):
        cfg = Config()

        assert cfg.ENV == "development"
        assert cfg.DEBUG is True
        assert cfg.DOCS == "docs"
        assert cfg.SQLALCHEMY_TRACK_MODIFICATIONS is False


def test_development_config_values():
    """Deve carregar corretamente valores da DevelopmentConfig"""
    env_vars = {
        "PORT_FLASK": "5001",
        "DOCS_DEV": "api-docs",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
    }

    with patch.dict(os.environ, env_vars, clear=True):
        from src.core import config

        importlib.reload(config)

        cfg = config.DevelopmentConfig()

        assert cfg.ENV == "development"
        assert cfg.DEBUG is True
        assert cfg.APPLICATION_ROOT == "/dev"
        assert cfg.PORT == "5001"
        assert cfg.DOCS == "api-docs"
        assert cfg.SQLALCHEMY_DATABASE_URI == "sqlite:///test.db"


def test_config_by_name_resolves_correct_class():
    """config_by_name deve retornar a classe correta"""
    assert config_by_name["development"] == DevelopmentConfig


def test_invalid_flask_env_raises_error():
    """Se FLASK_ENV for inválida, deve levantar ValueError"""

    with patch.dict(os.environ, {"FLASK_ENV": "invalid-env"}, clear=True):
        import src.core.config as config

        with pytest.raises(ValueError):
            importlib.reload(config)


def test_valid_flask_env_does_not_raise():
    """FLASK_ENV válida não deve levantar erro"""

    with patch.dict(os.environ, {"FLASK_ENV": "development"}, clear=True):
        import src.core.config as config

        # Reload garante que o código de validação execute novamente
        config = importlib.reload(config)

        assert config.flask_env == "development"
        assert "development" in config.config_by_name
