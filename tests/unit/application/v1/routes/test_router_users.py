from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException, status
from src.application.api.v1.schemas.users import UserOutSchema, UserUpdateBaseSchema
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


@pytest.mark.asyncio
async def test_update_user_success(client, override_dependency, generate_uuid):
    # Arrange: Configura mock para sucesso
    user_id = UUID(generate_uuid)  # Converte para UUID
    input_data = {'username': 'updated_user', 'email': 'updated@example.com'}
    mock_response = UserOutSchema(
        id=user_id,  # Usa o mesmo UUID
        username='updated_user',
        email='updated@example.com',
        role='user',  # Assuma role se necessário
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    override_dependency.update_user.return_value = mock_response

    # Act: Faz a requisição PATCH
    response = client.patch(f'/api/v1/users/{generate_uuid}', json=input_data)

    # Assert: Verifica status e resposta
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': str(mock_response.id),
        'username': 'updated_user',
        'email': 'updated@example.com',
        'role': 'user',
        'created_at': mock_response.created_at.isoformat(),
        'updated_at': mock_response.updated_at.isoformat(),
    }
    override_dependency.update_user.assert_called_once_with(
        user_id, UserUpdateBaseSchema(**input_data)
    )


def test_update_user_not_found(client, override_dependency, generate_uuid):
    # Arrange: Configura o mock para levantar HTTPException 404
    input_data = {
        'username': 'updated_user',
        'email': 'updated@example.com',
    }  # Dados válidos para passar validação
    override_dependency.update_user.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado'
    )

    # Act: Faz a requisição PATCH
    response = client.patch(f'/api/v1/users/{generate_uuid}', json=input_data)

    # Assert: Verifica status e detalhe
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado'


@pytest.mark.asyncio
async def test_update_user_validation_error(client, override_dependency, generate_uuid):
    # Arrange: Dados inválidos para UserUpdateBaseSchema (ex: email inválid)
    input_data = {
        'username': 'updated_user',
        'email': 'invalid-email',  # Assuma que valida EmailStr
    }

    # Act: Faz a requisição PATCH
    response = client.patch(f'/api/v1/users/{generate_uuid}', json=input_data)

    # Assert: Verifica erro de validação 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Pode assertar os detalhes do erro se quiser mais precisão
    assert 'detail' in response.json()


@pytest.mark.asyncio
async def test_delete_user_success(client, override_dependency, generate_uuid):
    # Arrange: Configura mock para sucesso (não retorna nada, só chama)
    user_id = UUID(generate_uuid)
    override_dependency.delete_user.return_value = (
        None  # Assume retorna None no sucesso
    )

    # Act: Faz a requisição DELETE
    response = client.delete(f'/api/v1/users/{generate_uuid}')

    # Assert: Verifica status 204 e chamada
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''  # No content
    override_dependency.delete_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_delete_user_not_found(client, override_dependency, generate_uuid):
    # Arrange: Configura o mock para levantar HTTPException 404
    override_dependency.delete_user.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado'
    )

    # Act: Faz a requisição DELETE
    response = client.delete(f'/api/v1/users/{generate_uuid}')

    # Assert: Verifica status e detalhe
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Usuário não encontrado'


@pytest.mark.asyncio
async def test_delete_user_invalid_uuid(client, override_dependency):
    # Act: UUID inválido no path (FastAPI valida automaticamente)
    response = client.delete('/api/v1/users/invalid-uuid')

    # Assert: Erro de validação 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()
