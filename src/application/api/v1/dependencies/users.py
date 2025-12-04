from typing import Annotated

from fastapi import Depends
from src.application.api.v1.controller.users import UsersController
from src.application.api.v1.dependencies.common.session import VerifiedSessionDep
from src.core.domain.service.users import UsersService
from src.core.domain.use_case.users import UsersUseCase
from src.infrastructure.repositories.users_postgres import UsersRepositoryPostgres


async def get_users_controller(
    session: VerifiedSessionDep,
) -> UsersController:
    """
    Singleton para o controller de usuários.
    """
    users_repository = UsersRepositoryPostgres(session)
    users_service = UsersService(users_repository)
    users_use_case = UsersUseCase(users_service)
    return UsersController(users_use_case)


UsersRepositoryDep = Annotated[UsersController, Depends(get_users_controller)]
