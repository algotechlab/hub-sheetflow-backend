from typing import List

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutDto,
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
