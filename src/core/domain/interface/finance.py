from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceOutByIdDto,
    FinanceOutDto,
    FinanceOutFlowBaseDto,
    FinanceOutFlowOutDto,
    HistoryFinanceDto,
    UpdatedFinanceOutFlowDto,
    UpdatedFinanceOutFlowOutDto,
    UpdateFinanceBaseDto,
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

    @abstractmethod
    async def list_finance_out_flow(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceOutFlowOutDto]: ...

    @abstractmethod
    async def get_finance_out_flow(self, outflow_id: UUID) -> FinanceOutFlowOutDto: ...

    @abstractmethod
    async def updated_finance_out_flow(
        self, outflow_id: UUID, outflow: UpdatedFinanceOutFlowDto
    ) -> UpdatedFinanceOutFlowOutDto: ...

    @abstractmethod
    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdDto | None: ...

    @abstractmethod
    async def get_history_finance(self, finace_id: UUID) -> HistoryFinanceDto: ...

    @abstractmethod
    async def update_finance(
        self, finance_id: UUID, finance: UpdateFinanceBaseDto
    ) -> FinanceOutDto | None: ...

    @abstractmethod
    async def delete_finance(self, finance_id: UUID) -> bool: ...
