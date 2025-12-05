import uuid

import pytest
from src.application.api.v1.schemas.groups import (
    GroupOutSchema,
)
from src.core.domain.dtos.groups import GroupBaseDto


@pytest.mark.asyncio
async def test_add_groups_success(
    groups_controller, mock_groups_use_case, generate_groups_schemas, mock_group_out_dto
):
    """Testa o sucesso da criação de um novo grupo."""
    input_schema = generate_groups_schemas
    expected_output = mock_group_out_dto

    mock_groups_use_case.add_groups.return_value = expected_output

    result = await groups_controller.add_groups(input_schema)
    mock_groups_use_case.add_groups.assert_awaited_once_with(
        GroupBaseDto(**input_schema.model_dump())
    )

    assert isinstance(result, GroupOutSchema)
    assert isinstance(result.id, uuid.UUID)
    assert result.id == expected_output.id
    assert result.name == 'Grupo 1'
    assert result.data['nome'] == 'JoeDoe'
    assert result.data['contato'] == '61994261245'
    assert len(result.custom_columns) == 1
    assert result.custom_columns[0].label == 'Idade'
    assert result.created_at is not None
    assert result.updated_at is not None
