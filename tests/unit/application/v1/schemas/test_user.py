from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError
from src.application.api.v1.schemas.users import UserBaseSchema, UserOutSchema


@pytest.mark.parametrize(
    ('username', 'email', 'password'),
    [
        ('johndoe123', 'john@example.com', 'strongpass123'),
        ('user1', 'user@test.com', 'password123456'),
    ],
)
def test_user_base_schema_valid(username, email, password):
    user = UserBaseSchema(username=username, email=email, password=password)

    assert user.username == username
    assert user.email == email
    assert user.password == password


@pytest.mark.parametrize(
    ('username', 'email', 'password', 'expected_error'),
    [
        (
            'jo',
            'john@example.com',
            'strongpass123',
            'String should have at least 3 characters',
        ),
        (
            'john doe',
            'john@example.com',
            'strongpass123',
            'username must be alphanumeric',
        ),
        (
            'johndoe123',
            'invalid',
            'strongpass123',
            'value is not a valid email address',
        ),
        (
            'johndoe123',
            'john@example.com',
            'a' * 256,
            'String should have at most 255 characters',
        ),
    ],
)
def test_user_base_schema_invalid(username, email, password, expected_error):
    with pytest.raises(ValidationError) as exc_info:
        UserBaseSchema(username=username, email=email, password=password)

    assert expected_error in str(exc_info.value)


def test_user_out_schema_valid():
    now = datetime.now()
    user_data = {
        'id': uuid4(),
        'username': 'johndoe123',
        'email': 'john@example.com',
        'role': 'admin',
        'created_at': now,
        'updated_at': now,
    }

    user_out = UserOutSchema(**user_data)

    assert user_out.id == user_data['id']
    assert user_out.username == user_data['username']
    assert user_out.email == user_data['email']
    assert user_out.role == user_data['role']
    assert user_out.created_at == now
    assert user_out.updated_at == now


def test_user_out_schema_invalid_missing_field():
    now = datetime.now()
    user_data = {
        'id': uuid4(),
        'username': 'johndoe123',
        'email': 'john@example.com',
        'created_at': now,
    }

    with pytest.raises(ValidationError) as exc_info:
        UserOutSchema(**user_data)

    assert 'updated_at' in str(exc_info.value)
    assert 'Field required' in str(exc_info.value)


def test_user_out_schema_from_attributes():
    class FakeORM:
        id = uuid4()
        username = 'johndoe123'
        email = 'john@example.com'
        role = 'admin'
        created_at = datetime.now()
        updated_at = datetime.now()

    fake_orm = FakeORM()

    user_out = UserOutSchema.model_validate(fake_orm)

    assert user_out.id == fake_orm.id
    assert user_out.username == fake_orm.username
    assert user_out.email == fake_orm.email
    assert user_out.role == fake_orm.role
    assert user_out.created_at == fake_orm.created_at
    assert user_out.updated_at == fake_orm.updated_at
