from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi import status
from src.application.api.v1.schemas.users import UserOutSchema
from src.core.domain.dtos.common.pagination import PaginationParamsDTO


@pytest.mark.asyncio
async def test_add_users_success(client, override_dependency):
    input_data = {
        'username': 'johndoe',
        'email': 'john@example.com',
        'password': 'password123',
    }
    now = datetime.now(timezone.utc)
    mock_response = UserOutSchema(
        id=uuid4(),
        username='johndoe',
        email='john@example.com',
        role='admin',
        created_at=now,
        updated_at=now,
    )
    override_dependency.add_users.return_value = mock_response

    response = client.post('/api/v1/users', json=input_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': str(mock_response.id),
        'username': 'johndoe',
        'email': 'john@example.com',
        'role': 'admin',
        'created_at': now.isoformat().replace('+00:00', 'Z'),
        'updated_at': now.isoformat().replace('+00:00', 'Z'),
    }
    override_dependency.add_users.assert_called_once()


@pytest.mark.asyncio
async def test_list_users_success_no_filter(client, override_dependency):
    result = 2
    mock_users = [
        UserOutSchema(
            id=uuid4(),
            username='user1',
            email='user1@example.com',
            role='admin',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        UserOutSchema(
            id=uuid4(),
            username='user2',
            email='user2@example.com',
            role='user',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    override_dependency.list_users.return_value = mock_users

    response = client.get('/api/v1/users')

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert len(json_response) == result
    assert json_response[0]['username'] == 'user1'
    assert json_response[1]['username'] == 'user2'
    override_dependency.list_users.assert_called_once_with(
        PaginationParamsDTO(filter_by=None, filter_value=None)
    )


@pytest.mark.asyncio
async def test_list_users_success_with_filter(client, override_dependency):
    result = 1
    mock_users = [
        UserOutSchema(
            id=uuid4(),
            username='johndoe',
            email='john@example.com',
            role='user',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ]
    override_dependency.list_users.return_value = mock_users

    response = client.get('/api/v1/users?filter_by=username&filter_value=johndoe')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert len(json_response) == result
    assert json_response[0]['username'] == 'johndoe'
    override_dependency.list_users.assert_called_once_with(
        PaginationParamsDTO(filter_by='username', filter_value='johndoe')
    )
