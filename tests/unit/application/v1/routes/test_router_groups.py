from fastapi import status
from src.application.api.v1.dependencies.groups import GroupsRepositoryDep
from src.application.api.v1.schemas.groups import (
    GroupOutSchema,
)


def test_add_groups_success(
    client, override_groups_dependency, generate_groups_schemas
):
    """Testa o sucesso da rota POST /groups (criação de grupo)."""
    body_data = generate_groups_schemas.model_dump()

    app = client.app
    app.dependency_overrides[GroupsRepositoryDep] = override_groups_dependency

    response = client.post(
        '/api/v1/groups', json=body_data, headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers['content-type'] == 'application/json'

    response_data = response.json()
    assert isinstance(response_data, dict)
    validated_response = GroupOutSchema.model_validate(response_data)
    assert validated_response.name == 'Grupo 1'
    assert validated_response.created_at is not None
    assert validated_response.updated_at is not None

    app.dependency_overrides.clear()
