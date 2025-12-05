from datetime import datetime
from typing import List
from uuid import uuid4

import pytest
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto


@pytest.mark.asyncio
async def test_add_users_success(users_service, mock_repository):
    # Arrange: Mock input DTO e resposta do repo
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_response = UserOutDto(
        id=uuid4(),
        username='johndoe',
        email='john@example.com',
        role='admin',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repository.add_users.return_value = mock_response

    result = await users_service.add_users(input_dto)

    mock_repository.add_users.assert_awaited_once_with(input_dto)
    assert result == mock_response
    assert isinstance(result, UserOutDto)


@pytest.mark.asyncio
async def test_add_users_handles_exception(users_service, mock_repository):
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_repository.add_users.side_effect = ValueError('Simulated repo error')

    with pytest.raises(ValueError, match='Simulated repo error'):
        await users_service.add_users(input_dto)

    mock_repository.add_users.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_users_success(users_service, mock_repository):
    count = 2
    # Arrange: Mock input DTO e resposta do repo
    input_dto = PaginationParamsDTO(filter_by='username', filter_value='john')
    mock_users = [
        UserOutDto(
            id=uuid4(),
            username='john1',
            email='john1@example.com',
            role='user',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        UserOutDto(
            id=uuid4(),
            username='john2',
            email='john2@example.com',
            role='admin',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    mock_repository.list_users.return_value = mock_users

    # Act: Chama o método do service
    result = await users_service.list_users(input_dto)

    # Assert: Verifica chamada ao repo e resultado
    mock_repository.list_users.assert_awaited_once_with(input_dto)
    assert result == mock_users
    assert isinstance(result, List)
    assert len(result) == count
    assert result[0].username == 'john1'
    assert result[1].username == 'john2'


@pytest.mark.asyncio
async def test_list_users_no_filter(users_service, mock_repository):
    # Arrange: Sem filtro
    input_dto = PaginationParamsDTO(filter_by=None, filter_value=None)
    mock_repository.list_users.return_value = []

    # Act
    result = await users_service.list_users(input_dto)

    # Assert: Lista vazia
    mock_repository.list_users.assert_awaited_once_with(input_dto)
    assert result == []


@pytest.mark.asyncio
async def test_list_users_handles_exception(users_service, mock_repository):
    # Arrange: Configura o repo pra levantar exceção
    input_dto = PaginationParamsDTO(filter_by='username', filter_value='john')
    mock_repository.list_users.side_effect = ValueError('Simulated repo error')

    # Act & Assert: Verifica se propaga a exceção
    with pytest.raises(ValueError, match='Simulated repo error'):
        await users_service.list_users(input_dto)

    mock_repository.list_users.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_success(users_service, mock_repository):
    # Arrange: Mock input DTO e resposta do repo (usuário atualizado)
    user_id = uuid4()
    input_dto = UpdateUserDto(username='updated_user', email='updated@example.com')
    mock_response = UserOutDto(
        id=user_id,
        username='updated_user',
        email='updated@example.com',
        role='user',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repository.update_user.return_value = mock_response

    # Act: Chama o método do service
    result = await users_service.update_user(user_id, input_dto)

    # Assert: Verifica chamada ao repo e resultado
    mock_repository.update_user.assert_awaited_once_with(user_id, input_dto)
    assert result == mock_response
    assert isinstance(result, UserOutDto)
