from typing import Annotated

from fastapi import Depends
from src.application.api.v1.controller.login import LoginController
from src.application.api.v1.dependencies.common.session import VerifiedSessionDep
from src.core.domain.service.login import LoginService
from src.core.domain.use_case.login import LoginUseCase
from src.infrastructure.repositories.login_postgres import LoginRepositoryPostgres


async def get_login_controller(
    session: VerifiedSessionDep,
) -> LoginController:
    """
    Singleton para o controller de login.
    """
    login_repository = LoginRepositoryPostgres(session)
    login_service = LoginService(login_repository)
    login_use_case = LoginUseCase(login_service)
    return LoginController(login_use_case)


LoginControllerDep = Annotated[LoginController, Depends(get_login_controller)]
