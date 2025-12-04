from datetime import datetime
from uuid import uuid4

import pytest
from src.core.domain.dtos.users import UserBaseDto, UserOutDto


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
