from datetime import datetime
from typing import List
from uuid import uuid4

import pytest
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.users import UpdateUserDto, UserBaseDto, UserOutDto
from src.core.domain.exceptions.users import (
    UserEmailDuplicatedException,
    UserNotFoundException,
)


@pytest.mark.asyncio
async def test_add_users_success(users_use_case, mock_service):
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
    mock_service.add_users.return_value = mock_response

    # Act: Chama o método do use case
    result = await users_use_case.add_users(input_dto)

    # Assert: Verifica chamada ao service e resultado
    mock_service.add_users.assert_awaited_once_with(input_dto)
    assert result == mock_response
    assert isinstance(result, UserOutDto)


@pytest.mark.asyncio
async def test_add_users_email_duplicated(users_use_case, mock_service):
    # Arrange: Configura o service pra levantar UserEmailDuplicatedException
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_service.add_users.side_effect = UserEmailDuplicatedException('Email duplicado')

    # Act & Assert: Verifica se relança com mensagem customizada
    with pytest.raises(UserEmailDuplicatedException) as exc_info:
        await users_use_case.add_users(input_dto)

    assert (
        str(exc_info.value)
        == f'Esse {input_dto.username} já está cadastrado com {input_dto.email}.'
    )
    mock_service.add_users.assert_awaited_once_with(input_dto)


@pytest.mark.asyncio
async def test_add_users_other_exception(users_use_case, mock_service):
    # Arrange: Configura o service pra levantar outra exceção
    input_dto = UserBaseDto(
        username='johndoe', email='john@example.com', password='password123'
    )
    mock_service.add_users.side_effect = ValueError('Outra erro simulado')

    # Act & Assert: Verifica se propaga a exceção original
    with pytest.raises(ValueError, match='Outra erro simulado'):
        await users_use_case.add_users(input_dto)

    mock_service.add_users.assert_awaited_once_with(input_dto)


@pytest.mark.asyncio
async def test_list_users_success(users_use_case, mock_service):
    count = 2
    # Arrange: Mock input DTO e resposta do service
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
    mock_service.list_users.return_value = mock_users

    # Act: Chama o método do use case
    result = await users_use_case.list_users(input_dto)

    # Assert: Verifica chamada ao service e resultado
    mock_service.list_users.assert_awaited_once_with(input_dto)
    assert result == mock_users
    assert isinstance(result, List)
    assert len(result) == count
    assert result[0].username == 'john1'
    assert result[1].username == 'john2'


@pytest.mark.asyncio
async def test_list_users_no_filter(users_use_case, mock_service):
    # Arrange: Sem filtro
    input_dto = PaginationParamsDTO(filter_by=None, filter_value=None)
    mock_service.list_users.return_value = []

    # Act
    result = await users_use_case.list_users(input_dto)

    # Assert: Lista vazia
    mock_service.list_users.assert_awaited_once_with(input_dto)
    assert result == []


@pytest.mark.asyncio
async def test_list_users_handles_exception(users_use_case, mock_service):
    # Arrange: Configura o service pra levantar exceção
    input_dto = PaginationParamsDTO(filter_by='username', filter_value='john')
    mock_service.list_users.side_effect = ValueError('Simulated service error')

    # Act & Assert: Verifica se propaga a exceção
    with pytest.raises(ValueError, match='Simulated service error'):
        await users_use_case.list_users(input_dto)

    mock_service.list_users.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_success(users_use_case, mock_service):
    # Arrange: Mock input DTO e resposta do service (usuário atualizado)
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
    mock_service.update_user.return_value = mock_response

    # Act: Chama o método do use case
    result = await users_use_case.update_user(user_id, input_dto)

    # Assert: Verifica chamada ao service e resultado
    mock_service.update_user.assert_awaited_once_with(user_id, input_dto)
    assert result == mock_response
    assert isinstance(result, UserOutDto)


@pytest.mark.asyncio
async def test_update_user_not_found(users_use_case, mock_service):
    # Arrange: Service retorna None (usuário não encontrado)
    user_id = uuid4()
    input_dto = UpdateUserDto(
        username='updated_user', email='updated@example.com'
    )  # Adicionei email obrigatório
    mock_service.update_user.return_value = None

    # Act & Assert: Levanta UserNotFoundException com mensagem correta
    with pytest.raises(
        UserNotFoundException, match=f'Esse {user_id} nao foi encontrado.'
    ):
        await users_use_case.update_user(user_id, input_dto)

    mock_service.update_user.assert_awaited_once_with(user_id, input_dto)
