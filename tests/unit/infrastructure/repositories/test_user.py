from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import IntegrityError
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import (
    DuplicatedException,
    UserEmailDuplicatedException,
)
from src.core.domain.models.users import User
from src.core.exceptions.custom import DatabaseException
from src.infrastructure.database.utils import PostgresErrorCode


@pytest.mark.asyncio
async def test_add_users_success(users_repo, mock_session):
    # Arrange: Mock input DTO e valores gerados

    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_id = uuid4()
    mock_role = 'admin'
    mock_created_at = datetime.now()
    mock_updated_at = datetime.now()

    # Simula o refresh setando os campos gerados (como o DB faria)
    async def simulate_refresh(user):
        user.id = mock_id
        user.role = mock_role
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


@pytest.mark.asyncio
async def test_list_users_success_no_filter(users_repo, mock_session):
    # Arrange: Mock input DTO sem filtro, resultado da query
    count = 2
    input_dto = PaginationParamsDTO(filter_by=None, filter_value=None)
    mock_rows = [
        MagicMock(
            _mapping={
                'id': uuid4(),
                'username': 'user1',
                'email': 'user1@example.com',
                'role': 'user',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }
        ),
        MagicMock(
            _mapping={
                'id': uuid4(),
                'username': 'user2',
                'email': 'user2@example.com',
                'role': 'admin',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }
        ),
    ]
    mock_result = MagicMock()
    mock_result.all.return_value = mock_rows
    mock_session.execute.return_value = mock_result

    # Act: Chama o método
    result = await users_repo.list_users(input_dto)

    # Assert: Verifica query sem filtro, ordem, e resultado
    actual_query = mock_session.execute.await_args[0][0]
    expected_query = (
        select(
            User.id,
            User.username,
            User.email,
            User.role,
            User.created_at,
            User.updated_at,
        )
        .where(User.is_deleted.__eq__(False))
        .order_by(User.created_at)
    )
    assert str(actual_query) == str(expected_query)
    assert len(result) == count
    assert result[0].username == 'user1'
    assert result[1].username == 'user2'
    mock_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_list_users_success_with_filter(users_repo, mock_session):
    # Arrange: Com filtro
    input_dto = PaginationParamsDTO(filter_by='username', filter_value='john')
    mock_rows = [
        MagicMock(
            _mapping={
                'id': uuid4(),
                'username': 'john',
                'email': 'john@example.com',
                'role': 'user',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }
        )
    ]
    mock_result = MagicMock()
    mock_result.all.return_value = mock_rows
    mock_session.execute.return_value = mock_result

    # Act
    result = await users_repo.list_users(input_dto)

    # Assert: Query com filtro
    actual_query = mock_session.execute.await_args[0][0]
    expected_query = (
        select(
            User.id,
            User.username,
            User.email,
            User.role,
            User.created_at,
            User.updated_at,
        )
        .where(User.is_deleted.__eq__(False))
        .order_by(User.created_at)
        .filter(User.username == 'john')
    )
    assert str(actual_query) == str(expected_query)
    assert len(result) == 1
    assert result[0].username == 'john'
    mock_session.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_list_users_exception(users_repo, mock_session):
    # Arrange: Simula exceção na execute
    input_dto = PaginationParamsDTO(filter_by=None, filter_value=None)
    mock_session.execute.side_effect = ValueError('Simulated DB error')

    # Act & Assert: Levanta DatabaseException e rollback
    with pytest.raises(DatabaseException, match='Simulated DB error'):
        await users_repo.list_users(input_dto)

    mock_session.rollback.assert_awaited_once()
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_success(users_repo, mock_session):
    # Arrange: Mock input DTO, stmt, e resposta (usuário atualizado)
    user_id = uuid4()
    input_dto = UpdateUserDto(username='updated_user', email='updated@example.com')
    mock_updated_user = MagicMock(
        id=user_id,
        username='updated_user',
        email='updated@example.com',
        role='user',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_updated_user
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    # Act: Chama o método
    result = await users_repo.update_user(user_id, input_dto)

    # Assert: Verifica stmt com valores corretos, commit, e resultado
    actual_stmt = mock_session.execute.await_args[0][0]
    expected_values = input_dto.model_dump(
        exclude_unset=True
    )  # Deve ser {'username': 'updated_user', 'email': 'updated@example.com'}
    assert str(actual_stmt) == str(
        sqlalchemy_update(User)
        .where(User.id == user_id)
        .values(**expected_values)
        .returning(User)
    )
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_called()
    assert isinstance(result, UserOutDto)
    assert result.id == user_id
    assert result.username == 'updated_user'
    assert result.email == 'updated@example.com'


@pytest.mark.asyncio
async def test_update_user_not_found(users_repo, mock_session):
    # Arrange: Repo retorna None (sem rows afetadas)
    user_id = uuid4()
    input_dto = UpdateUserDto(username='updated_user', email='updated@example.com')
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    # Act
    result = await users_repo.update_user(user_id, input_dto)

    # Assert: Retorna None, commit ainda chamado (mas sem changes)
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_called()
    assert result is None


@pytest.mark.asyncio
async def test_update_user_exception(users_repo, mock_session):
    # Arrange: Simula exceção na execute
    user_id = uuid4()
    input_dto = UpdateUserDto(username='updated_user', email='updated@example.com')
    mock_session.execute.side_effect = ValueError('Simulated DB error')

    # Act & Assert: Levanta DatabaseException e rollback
    with pytest.raises(DatabaseException, match='Simulated DB error'):
        await users_repo.update_user(user_id, input_dto)

    mock_session.rollback.assert_awaited_once()
    mock_session.commit.assert_not_awaited()
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_success(users_repo, mock_session):
    # Arrange: Mock user_id, stmt, e resposta (usuário atualizado)
    user_id = uuid4()
    mock_updated_user = MagicMock(id=user_id, is_deleted=True)  # Simula após update
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_updated_user
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    # Act: Chama o método
    result = await users_repo.delete_user(user_id)

    actual_stmt = mock_session.execute.await_args[0][0]
    expected_stmt = (
        sqlalchemy_update(User)
        .where(User.id.__eq__(user_id), User.is_deleted.__eq__(False))
        .values(is_deleted=True)
        .returning(User)
    )
    assert str(actual_stmt) == str(expected_stmt)
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_called()
    assert result is True


@pytest.mark.asyncio
async def test_delete_user_not_found_or_already_deleted(users_repo, mock_session):
    # Arrange: Sem rows afetadas (não encontrado ou já deletado)
    user_id = uuid4()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    mock_session.commit.return_value = None

    # Act
    result = await users_repo.delete_user(user_id)

    # Assert: Commit ainda chamado, mas retorna False
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_called()
    assert result is False


@pytest.mark.asyncio
async def test_delete_user_exception(users_repo, mock_session):
    # Arrange: Simula exceção na execute
    user_id = uuid4()
    mock_session.execute.side_effect = ValueError('Simulated DB error')

    # Act & Assert: Levanta DatabaseException e rollback
    with pytest.raises(DatabaseException, match='Simulated DB error'):
        await users_repo.delete_user(user_id)

    mock_session.rollback.assert_awaited_once()
    mock_session.commit.assert_not_awaited()
    mock_session.execute.assert_awaited_once()
