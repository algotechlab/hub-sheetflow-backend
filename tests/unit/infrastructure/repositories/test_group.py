import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.domain.dtos.groups import GroupBaseDto, GroupOutDto
from src.core.domain.models.groups import Groups
from src.core.exceptions.custom import DatabaseException
from src.infrastructure.repositories.groups_postgres import GroupsRepositoriesPostgres


@pytest.fixture
def mock_async_session():
    """Mock para AsyncSession (com métodos async mockados)."""
    session = AsyncMock(spec=AsyncSession)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def groups_repository(mock_async_session):
    """Fixture para o repositório de grupos."""
    return GroupsRepositoriesPostgres(session=mock_async_session)


@pytest.fixture
def generate_group_base_dto():
    """Fixture para DTO de entrada de grupo (alinhado com GroupBaseDto)."""
    return GroupBaseDto(
        name='Grupo 1',
        data={
            'observacao': 'Deixando os clientes mais livres',
            'local': 'SERRA',
            'nome': 'JoeDoe',
            'contato': '61994261245',
            'cpfCnpj': '06472580138',
            'pastaDrive': 'DRIVE',
            'vara': 'Financeiro',
            'custom_1': '30',
        },
        custom_columns=[
            {
                'name': 'custom_1',
                'label': 'Idade',
                'type': 'text',
            }
        ],
    )


@pytest.fixture
def mock_groups_model(generate_group_base_dto):
    """Mock para o modelo Groups (simula criação e validação)."""
    fake_id = uuid.uuid4()
    mock_model = MagicMock(spec=Groups)
    mock_model.id = fake_id
    mock_model.name = generate_group_base_dto.name
    mock_model.data = generate_group_base_dto.data
    mock_model.custom_columns = generate_group_base_dto.custom_columns
    mock_model.created_at = datetime.now()
    mock_model.updated_at = datetime.now()

    with patch(
        'src.core.domain.dtos.groups.GroupOutDto.model_validate'
    ) as mock_validate:
        mock_validate.return_value = GroupOutDto(
            id=fake_id,
            name=generate_group_base_dto.name,
            data=generate_group_base_dto.data,
            custom_columns=generate_group_base_dto.custom_columns,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        yield mock_model
        mock_validate.assert_called_once_with(mock_model)


@pytest.mark.asyncio
async def test_add_groups_success(
    groups_repository, mock_async_session, generate_group_base_dto
):
    """Testa o sucesso da adição de um grupo no repositório."""
    mock_async_session.commit.return_value = None
    mock_async_session.refresh.return_value = None

    mock_db_groups = MagicMock(spec=Groups)
    fake_id = uuid.uuid4()
    mock_db_groups.id = fake_id
    mock_db_groups.name = generate_group_base_dto.name
    mock_db_groups.data = generate_group_base_dto.data
    mock_db_groups.custom_columns = generate_group_base_dto.custom_columns
    mock_db_groups.created_at = datetime.now()
    mock_db_groups.updated_at = datetime.now()

    # Cria mock para o output DTO
    expected_output = GroupOutDto(
        id=fake_id,
        name=generate_group_base_dto.name,
        data=generate_group_base_dto.data,
        custom_columns=generate_group_base_dto.custom_columns,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    with patch(
        'src.infrastructure.repositories.groups_postgres.Groups',
        return_value=mock_db_groups,
    ):
        # Patch para model_validate retornar o DTO esperado
        with patch(
            'src.core.domain.dtos.groups.GroupOutDto.model_validate',
            return_value=expected_output,
        ):
            # Chama o método do repositório
            result = await groups_repository.add_groups(generate_group_base_dto)

    # Verifica chamadas no session (agora add é chamado com o mock_db_groups do patch)
    mock_async_session.add.assert_called_once_with(mock_db_groups)
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once_with(mock_db_groups)
    mock_async_session.rollback.assert_not_called()  # Não rolou erro

    # Asserções no resultado (GroupOutDto)
    assert result == expected_output
    assert isinstance(result, GroupOutDto)
    assert isinstance(result.id, uuid.UUID)
    assert result.name == 'Grupo 1'
    assert result.data['nome'] == 'JoeDoe'
    assert result.data['contato'] == '61994261245'
    assert len(result.custom_columns) == 1
    assert result.custom_columns[0]['label'] == 'Idade'  # Dict, então ['label']
    assert result.created_at is not None
    assert result.updated_at is not None


@pytest.mark.asyncio
async def test_add_groups_database_error(
    groups_repository, mock_async_session, generate_group_base_dto
):
    """
    Testa o tratamento de erro de banco no add_groups
    (rola rollback e levanta DatabaseException).
    """
    mock_async_session.commit.side_effect = SQLAlchemyError('Erro simulado no DB')

    with patch('src.core.domain.models.groups.Groups'):
        with pytest.raises(DatabaseException) as exc_info:
            await groups_repository.add_groups(generate_group_base_dto)

    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.rollback.assert_awaited_once()  # Rola rollback
    mock_async_session.refresh.assert_not_called()

    assert 'Erro simulado no DB' in str(exc_info.value)
