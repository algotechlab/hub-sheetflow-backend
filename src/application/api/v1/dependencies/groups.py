from typing import Annotated

from fastapi import Depends
from src.application.api.v1.controller.groups import GroupsController
from src.application.api.v1.dependencies.common.session import VerifiedSessionDep
from src.core.domain.service.groups import GroupsService
from src.core.domain.use_case.groups import GroupsUseCase
from src.infrastructure.repositories.groups_postgres import GroupsRepositoriesPostgres


async def get_groups_controller(
    session: VerifiedSessionDep,
) -> GroupsController:
    """
    Singleton para o controller de grupos.
    """
    groups_repository = GroupsRepositoriesPostgres(session)
    groups_service = GroupsService(groups_repository)
    groups_use_case = GroupsUseCase(groups_service)
    return GroupsController(groups_use_case)


GroupsRepositoryDep = Annotated[GroupsController, Depends(get_groups_controller)]
