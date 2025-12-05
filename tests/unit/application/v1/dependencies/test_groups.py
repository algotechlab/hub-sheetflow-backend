import pytest
from src.application.api.v1.controller.groups import GroupsController
from src.application.api.v1.dependencies.groups import get_groups_controller


class DummySession:
    pass


@pytest.mark.asyncio
async def test_get_groups_controller_returns_instance():
    session = DummySession()

    controller = await get_groups_controller(session)  # executa dependência

    assert isinstance(controller, GroupsController)
