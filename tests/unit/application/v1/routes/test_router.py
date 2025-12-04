from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi import status
from src.application.api.v1.schemas.users import UserOutSchema


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
