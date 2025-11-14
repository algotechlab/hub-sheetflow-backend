from unittest.mock import patch

import pytest
from sqlalchemy.exc import OperationalError

from src.db.extensions import verify_database_connection


def test_verify_connection_success(fake_app):
    """Conexão de sucesso na primeira tentativa"""
    with patch("src.db.extensions.db") as mock_db:
        mock_db.session.execute.return_value = True

        result = verify_database_connection(fake_app)

        assert result is True
        mock_db.session.execute.assert_called_once()


def test_verify_connection_retry_success(fake_app):
    """Falha na primeira tentativa, sucesso na segunda"""

    with (
        patch("src.db.extensions.db") as mock_db,
        patch("time.sleep") as mock_sleep,
    ):

        mock_db.session.execute.side_effect = [
            OperationalError("Fail", None, None),
            True,
        ]

        result = verify_database_connection(fake_app, retries=2, delay=1)

        assert result is True
        assert mock_db.session.execute.call_count == 2
        mock_sleep.assert_called_once_with(1)


def test_verify_connection_failure(fake_app):
    """Falha total após todas as tentativas"""

    with (
        patch("src.db.extensions.db") as mock_db,
        patch("time.sleep") as mock_sleep,
    ):
        mock = OperationalError("Fail", None, None)
        mock_db.session.execute.side_effect = mock

        with pytest.raises(OperationalError):
            verify_database_connection(fake_app, retries=3, delay=1)

        assert mock_db.session.execute.call_count == 3
        assert mock_sleep.call_count == 2
