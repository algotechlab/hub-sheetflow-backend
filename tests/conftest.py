import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from src.application.api.v1.controller.groups import GroupsController
from src.application.api.v1.controller.users import UsersController
from src.application.api.v1.dependencies.users import get_users_controller
from src.application.api.v1.schemas.groups import CustomColumn, GroupBaseSchema
from src.core.config.settings import get_settings
from src.core.domain.dtos.groups import GroupOutDto
from src.core.domain.interface.users import UsersRepositoriesInterface
from src.core.domain.service.users import UsersService
from src.core.domain.use_case.groups import GroupsUseCase
from src.core.domain.use_case.users import UsersUseCase
from src.infrastructure.repositories.users_postgres import UsersRepositoryPostgres
from src.main import app


@pytest.fixture
def generate_uuid():
    return str(uuid.uuid4())


@pytest.fixture
def mock_use_case():
    return AsyncMock(spec=UsersUseCase)


@pytest.fixture
def users_controller(mock_use_case):
    return UsersController(use_case=mock_use_case)


@pytest.fixture
def override_dependency():
    mock_controller = AsyncMock(spec=UsersController)
    app.dependency_overrides[get_users_controller] = lambda: mock_controller
    yield mock_controller
    app.dependency_overrides = {}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_env(monkeypatch):
    # Fixture para mockar variáveis de ambiente
    def set_env(vars_dict):
        for key, value in vars_dict.items():
            monkeypatch.setenv(key, value)

    return set_env


@pytest.fixture
def clear_cache():
    # Limpa o cache do lru_cache antes de cada teste
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=UsersRepositoriesInterface)


@pytest.fixture
def users_service(mock_repository):
    return UsersService(users_repository=mock_repository)


@pytest.fixture
def mock_service():
    return AsyncMock(spec=UsersService)


@pytest.fixture
def users_use_case(mock_service):
    return UsersUseCase(users_service=mock_service)


@pytest.fixture
def users_repo(mock_session):
    return UsersRepositoryPostgres(session=mock_session)


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def generate_groups_schemas():
    """
    Fixture para schema de entrada de grupo
    (alinhado com GroupBaseSchema e GroupBaseDto).
    """
    return GroupBaseSchema(
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
        custom_columns=[CustomColumn(name='custom_1', label='Idade', type='text')],
    )


@pytest.fixture
def mock_groups_use_case():
    """Mock para o use case de grupos (AsyncMock para métodos async)."""
    return AsyncMock(spec=GroupsUseCase)


@pytest.fixture
def groups_controller(mock_groups_use_case):
    """Fixture para o controller de grupos."""
    return GroupsController(use_case=mock_groups_use_case)


@pytest.fixture
def mock_group_out_dto(generate_groups_schemas):
    """Fixture para DTO de saída de grupo (alinhado com GroupOutDto)."""
    input_schema = generate_groups_schemas
    fake_id = uuid.uuid4()

    custom_cols_dicts = [col.model_dump() for col in input_schema.custom_columns]

    return GroupOutDto(
        id=fake_id,
        name=input_schema.name,
        data=input_schema.data,
        custom_columns=custom_cols_dicts,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def override_groups_dependency(mock_groups_use_case):
    """Override para a dependência GroupsRepositoryDep (retorna mocked controller)."""

    async def override_dependency():
        return GroupsController(use_case=mock_groups_use_case)

    return override_dependency
