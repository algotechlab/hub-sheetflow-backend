from typing import List
from uuid import UUID

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutByIdDto,
    FinanceOutDto,
    FinanceOutFlowBaseDto,
    FinanceOutFlowOutDto,
    HistoryFinanceDto,
    UpdatedFinanceInstallNumbersDto,
    UpdatedFinanceInstallNumbersOutDto,
    UpdatedFinanceOutFlowDto,
    UpdatedFinanceOutFlowOutDto,
    UpdateFinanceBaseDto,
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

    async def list_finance_out_flow(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceOutFlowOutDto]:
        return await self.finance_repository.list_finance_out_flow(pagination)

    async def get_finance_out_flow(self, outflow_id: UUID) -> FinanceOutFlowOutDto:
        return await self.finance_repository.get_finance_out_flow(outflow_id)

    async def updated_finance_out_flow(
        self, outflow_id: UUID, outflow: UpdatedFinanceOutFlowDto
    ) -> UpdatedFinanceOutFlowOutDto:
        return await self.finance_repository.updated_finance_out_flow(
            outflow_id, outflow
        )

    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBaseDto
    ) -> FinanceOutFlowOutDto:
        return await self.finance_repository.add_finance_outflow(finance_outflow)

    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdDto:
        return await self.finance_repository.get_finance(finance_id)

    async def get_history_finance(self, finace_id: UUID) -> HistoryFinanceDto:
        return await self.finance_repository.get_history_finance(finace_id)

    async def update_finance(
        self, finance_id: UUID, finance: UpdateFinanceBaseDto
    ) -> FinanceOutDto:
        return await self.finance_repository.update_finance(finance_id, finance)

    async def updated_finance_install_numbers(
        self, finance_id: UUID, install_numbers: UpdatedFinanceInstallNumbersDto
    ) -> UpdatedFinanceInstallNumbersOutDto:
        return await self.finance_repository.updated_finance_install_numbers(
            finance_id, install_numbers
        )

    async def delete_finance(self, finance_id: UUID) -> bool:
        return await self.finance_repository.delete_finance(finance_id)
