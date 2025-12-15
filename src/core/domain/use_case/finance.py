from typing import List

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutDto,
    FinanceOutFlowBaseDto,
    FinanceOutFlowOutDto,
)
from src.core.domain.service.finance import FinanceService


class FinanceUseCase:
    def __init__(self, finance_service: FinanceService):
        self.finance_service = finance_service

    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto:
        return await self.finance_service.add_finance(finance)

    async def list_finance(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceListOutDto]:
        return await self.finance_service.list_finance(pagination)

    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBaseDto
    ) -> FinanceOutFlowOutDto:
        return await self.finance_service.add_finance_outflow(finance_outflow)
