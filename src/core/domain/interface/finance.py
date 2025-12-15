from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceOutDto,
    FinanceOutFlowBaseDto,
    FinanceOutFlowOutDto,
)


class FinanceRepositoriesInterface(ABC):
    @abstractmethod
    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto: ...

    @abstractmethod
    async def list_finance(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceOutDto]: ...

    @abstractmethod
    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBaseDto
    ) -> FinanceOutFlowOutDto: ...
