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
    UpdatedFinanceOutFlowInstallNumbersDto,
    UpdatedFinanceOutFlowInstallNumbersOutDto,
    UpdatedFinanceOutFlowOutDto,
    UpdateFinanceBaseDto,
)
from src.core.domain.exceptions.finance import FinanceNotFoundException
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

    async def list_finance_out_flow(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceOutFlowOutDto]:
        return await self.finance_service.list_finance_out_flow(pagination)

    async def get_finance_out_flow(
        self, outflow_id: UUID
    ) -> FinanceOutFlowOutDto | None:
        return await self.finance_service.get_finance_out_flow(outflow_id)

    async def updated_finance_out_flow(
        self, outflow_id: UUID, outflow: UpdatedFinanceOutFlowDto
    ) -> UpdatedFinanceOutFlowOutDto:
        return await self.finance_service.updated_finance_out_flow(outflow_id, outflow)

    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBaseDto
    ) -> FinanceOutFlowOutDto:
        return await self.finance_service.add_finance_outflow(finance_outflow)

    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdDto:
        return await self.finance_service.get_finance(finance_id)

    async def get_history_finance(self, finace_id: UUID) -> HistoryFinanceDto:
        return await self.finance_service.get_history_finance(finace_id)

    async def update_finance(
        self, finance_id: UUID, finance: UpdateFinanceBaseDto
    ) -> FinanceOutDto:
        result = await self.finance_service.update_finance(finance_id, finance)
        if result is None:
            raise FinanceNotFoundException(f'Esse {finance_id} não foi encontrado.')
        return result

    async def updated_finance_install_numbers(
        self, finance_id: UUID, install_numbers: UpdatedFinanceInstallNumbersDto
    ) -> UpdatedFinanceInstallNumbersOutDto:
        return await self.finance_service.updated_finance_install_numbers(
            finance_id, install_numbers
        )

    async def updated_finance_out_flow_install_numbers(
        self,
        finance_out_flow_box_id: UUID,
        finance_out_flow: UpdatedFinanceOutFlowInstallNumbersDto,
    ) -> UpdatedFinanceOutFlowInstallNumbersOutDto:
        return await self.finance_service.updated_finance_out_flow_install_numbers(
            finance_out_flow_box_id, finance_out_flow
        )

    async def delete_finance(self, finance_id: UUID) -> None:
        result = await self.finance_service.delete_finance(finance_id)

        if result is None:
            raise FinanceNotFoundException(f'Esse {finance_id} não foi encontrado.')
