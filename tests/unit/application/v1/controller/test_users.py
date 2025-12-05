import uuid
from datetime import datetime
from typing import List
from unittest.mock import MagicMock

import pytest
from src.application.api.v1.schemas.common.pagination import PaginationParamsBaseSchema
from src.application.api.v1.schemas.users import (
    UserBaseSchema,
    UserOutSchema,
    UserUpdateBaseSchema,
)
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto


@pytest.mark.asyncio
async def test_add_users_success(users_controller, mock_use_case):
    """Testa o sucesso da criação de um novo usuário"""
    input_schema = UserBaseSchema(
        username='johndoe', email='john@example.com', password='password123'
    )
    expected_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_response = MagicMock()
    mock_response.id = uuid.uuid4()
    mock_response.username = 'johndoe'
    mock_response.email = 'john@example.com'
    mock_response.role = 'admin'

    mock_use_case.add_users.return_value = mock_response

    result = await users_controller.add_users(input_schema)

    mock_use_case.add_users.assert_awaited_once_with(expected_dto)

    assert isinstance(result, UserOutSchema)
    assert isinstance(result.id, uuid.UUID)
    assert result.username == 'johndoe'
    assert result.email == 'john@example.com'


@pytest.mark.asyncio
async def test_add_users_handles_exception(users_controller, mock_use_case):
    """Testa o tratamento de exceções na criação de um novo usuário"""
    input_schema = UserBaseSchema(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_use_case.add_users.side_effect = ValueError('Simulated use case error')

    with pytest.raises(ValueError, match='Simulated use case error'):
        await users_controller.add_users(input_schema)

    mock_use_case.add_users.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_users_success(users_controller, mock_use_case, generate_uuid):
    count = 2
    input_schema = PaginationParamsBaseSchema(filter_by='username', filter_value='john')
    expected_dto = PaginationParamsDTO(filter_by='username', filter_value='john')
    mock_users = [
        MagicMock(
            id=generate_uuid,
            username='john1',
            email='john1@example.com',
            role='user',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        MagicMock(
            id=generate_uuid,
            username='john2',
            email='john2@example.com',
            role='admin',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_use_case.list_users.return_value = mock_users

    # Act: Chama o método do controller
    result = await users_controller.list_users(input_schema)

    # Assert: Verifica a conversão, chamada e resultado
    mock_use_case.list_users.assert_awaited_once_with(expected_dto)
    assert isinstance(result, List)
    assert len(result) == count
    assert isinstance(result[0], UserOutSchema)
    assert result[0].username == 'john1'
    assert result[1].username == 'john2'


@pytest.mark.asyncio
async def test_list_users_no_filter(users_controller, mock_use_case):
    # Arrange: Sem filtro
    input_schema = PaginationParamsBaseSchema()
    expected_dto = PaginationParamsDTO(filter_by=None, filter_value=None)
    mock_use_case.list_users.return_value = []

    # Act
    result = await users_controller.list_users(input_schema)

    # Assert: Lista vazia
    mock_use_case.list_users.assert_awaited_once_with(expected_dto)
    assert result == []


@pytest.mark.asyncio
async def test_list_users_handles_exception(users_controller, mock_use_case):
    # Arrange: Configura o use_case pra levantar exceção
    input_schema = PaginationParamsBaseSchema()
    mock_use_case.list_users.side_effect = ValueError('Simulated use case error')

    # Act & Assert: Verifica se propaga a exceção
    with pytest.raises(ValueError, match='Simulated use case error'):
        await users_controller.list_users(input_schema)

    mock_use_case.list_users.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_success(users_controller, mock_use_case):
    # Arrange: Mock input schema, DTO e resposta do use_case
    user_id = uuid.uuid4()
    input_schema = UserUpdateBaseSchema(
        username='updated_user', email='updated@example.com'
    )  # Assuma campos opcionais
    expected_dto = UpdateUserDto(username='updated_user', email='updated@example.com')
    mock_response = MagicMock(
        id=user_id,
        username='updated_user',
        email='updated@example.com',
        role='user',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_use_case.update_user.return_value = mock_response

    # Act: Chama o método do controller
    result = await users_controller.update_user(user_id, input_schema)

    # Assert: Verifica a conversão, chamada e resultado
    mock_use_case.update_user.assert_awaited_once_with(user_id, expected_dto)
    assert isinstance(result, UserOutSchema)
    assert result.id == user_id
    assert result.username == 'updated_user'
    assert result.email == 'updated@example.com'


@pytest.mark.asyncio
async def test_delete_user_success(users_controller, mock_use_case):
    # Arrange: Mock user_id e use_case retorna None (sucesso)
    user_id = uuid.uuid4()
    mock_use_case.delete_user.return_value = None

    # Act: Chama o método do controller
    result = await users_controller.delete_user(user_id)

    # Assert: Verifica chamada ao use_case e retorno None
    mock_use_case.delete_user.assert_awaited_once_with(user_id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_user_handles_exception(users_controller, mock_use_case):
    # Arrange: Configura o use_case pra levantar exceção
    user_id = uuid.uuid4()
    mock_use_case.delete_user.side_effect = ValueError('Simulated use case error')

    # Act & Assert: Verifica se propaga a exceção
    with pytest.raises(ValueError, match='Simulated use case error'):
        await users_controller.delete_user(user_id)

    mock_use_case.delete_user.assert_awaited_once()
