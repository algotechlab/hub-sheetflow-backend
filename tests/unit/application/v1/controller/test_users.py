import uuid
from unittest.mock import MagicMock

import pytest
from src.application.api.v1.schemas.users import UserBaseSchema, UserOutSchema
from src.core.domain.dtos.users import UserBaseDto


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
