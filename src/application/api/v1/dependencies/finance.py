from typing import Annotated

from fastapi import Depends
from src.application.api.v1.controller.finance import FinanceController
from src.application.api.v1.dependencies.common.session import VerifiedSessionDep
from src.core.domain.service.finance import FinanceService
from src.core.domain.use_case.finance import FinanceUseCase
from src.infrastructure.repositories.finance_postgres import FinanceRepositoriesPostgres


async def get_finance_controller(
    session: VerifiedSessionDep,
) -> FinanceController:
    """
    Singleton para o controller de grupos.
    """
    finance_repository = FinanceRepositoriesPostgres(session)
    finance_service = FinanceService(finance_repository)
    finance_use_case = FinanceUseCase(finance_service)
    return FinanceController(finance_use_case)


FinanceRepositoryDep = Annotated[FinanceController, Depends(get_finance_controller)]
