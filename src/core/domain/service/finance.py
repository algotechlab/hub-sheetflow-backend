from typing import List
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutDto,
    FinanceOutFlowBaseDto,
    FinanceOutFlowOutDto,
)
from src.core.domain.interface.finance import FinanceRepositoriesInterface


class FinanceService:
    def __init__(self, finance_repository: FinanceRepositoriesInterface):
        self.finance_repository = finance_repository

    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto:
        return await self.finance_repository.add_finance(finance)

    async def list_finance(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceListOutDto]:
        return await self.finance_repository.list_finance(pagination)

    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBaseDto
    ) -> FinanceOutFlowOutDto:
        return await self.finance_repository.add_finance_outflow(finance_outflow)

    async def delete_finance(self, finance_id: UUID) -> bool:
        return await self.finance_repository.delete_finance(finance_id)
