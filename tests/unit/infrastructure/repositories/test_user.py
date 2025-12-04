from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from src.core.domain.dtos.users import UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import (
    DuplicatedException,
    UserEmailDuplicatedException,
)
from src.core.exceptions.custom import DatabaseException
from src.infrastructure.database.utils import PostgresErrorCode


@pytest.mark.asyncio
async def test_add_users_success(users_repo, mock_session):
    # Arrange: Mock input DTO e valores gerados

    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_id = uuid4()
    mock_created_at = datetime.now()
    mock_updated_at = datetime.now()

    # Simula o refresh setando os campos gerados (como o DB faria)
    async def simulate_refresh(user):
        user.id = mock_id
        user.created_at = mock_created_at
        user.updated_at = mock_updated_at

    mock_session.refresh.side_effect = simulate_refresh
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    # Act: Chama o método (o User real será criado internamente)
    result = await users_repo.add_users(input_dto)

    # Assert: Verifica chamadas e resultado
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    mock_session.rollback.assert_not_called()
    assert isinstance(result, UserOutDto)
    assert result.id == mock_id
    assert result.username == 'johndoe'
    assert result.email == 'john@example.com'
    assert result.created_at == mock_created_at
    assert result.updated_at == mock_updated_at


@pytest.mark.asyncio
async def test_add_users_email_duplicated(users_repo, mock_session):
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )

    mock_orig = MagicMock()
    mock_orig.pgcode = PostgresErrorCode.UNIQUE_VIOLATION
    mock_orig.__str__.return_value = 'unique constraint on email'
    mock_session.commit.side_effect = IntegrityError('stmt', 'params', mock_orig)

    with pytest.raises(UserEmailDuplicatedException):
        await users_repo.add_users(input_dto)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_awaited_once()
    mock_session.refresh.assert_not_called()


@pytest.mark.asyncio
async def test_add_users_other_duplicated(users_repo, mock_session):
    # Arrange: Mock input DTO e User
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_user = MagicMock()

    with patch('src.core.domain.models.users.User', return_value=mock_user):
        # Simula IntegrityError com UNIQUE_VIOLATION mas sem 'email' no detail
        mock_orig = MagicMock()
        mock_orig.pgcode = PostgresErrorCode.UNIQUE_VIOLATION
        mock_orig.__str__.return_value = 'unique constraint on other field'
        mock_session.commit.side_effect = IntegrityError('stmt', 'params', mock_orig)

        # Act & Assert: Verifica se levanta DuplicatedException
        with pytest.raises(DuplicatedException):
            await users_repo.add_users(input_dto)

        mock_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_users_integrity_no_pgcode(users_repo, mock_session):
    # Arrange: IntegrityError sem orig.pgcode
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_user = MagicMock()

    with patch('src.core.domain.models.users.User', return_value=mock_user):
        mock_session.commit.side_effect = IntegrityError('stmt', 'params', None)

        # Act & Assert: Levanta DuplicatedException com msg genérica
        with pytest.raises(DuplicatedException):
            await users_repo.add_users(input_dto)

        mock_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_users_general_exception(users_repo, mock_session):
    # Arrange: Outra exceção (ex: ValueError)
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_user = MagicMock()

    with patch('src.core.domain.models.users.User', return_value=mock_user):
        mock_session.commit.side_effect = ValueError('General error')

        # Act & Assert: Levanta DatabaseException
        with pytest.raises(DatabaseException, match='General error'):
            await users_repo.add_users(input_dto)

        mock_session.rollback.assert_awaited_once()
