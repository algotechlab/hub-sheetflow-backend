from typing import List
from uuid import UUID

from src.application.api.v1.schemas.common.pagination import PaginationParamsBaseSchema
from src.application.api.v1.schemas.finance import (
    FinanceBaseSchema,
    FinanceListInSchema,
    FinanceOutByIdSchema,
    FinanceOutFlowBaseSchema,
    FinanceOutFlowOutSchema,
    FinanceOutSchema,
    UpdatedFinanceOutFlowOutSchema,
    UpdatedFinanceOutFlowSchema,
)
from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceOutFlowBaseDto,
    UpdateFinanceBaseDto,
)
from src.core.domain.use_case.finance import FinanceUseCase


class FinanceController:
    def __init__(self, use_case: FinanceUseCase):
        self.use_case = use_case

    async def add_finance(self, finance: FinanceBaseSchema) -> FinanceOutSchema:
        finance_dto = FinanceBaseDto(**finance.model_dump())
        finance_case = await self.use_case.add_finance(finance_dto)
        return FinanceOutSchema.model_validate(finance_case)

    async def list_finance(
        self, pagination: PaginationParamsBaseSchema
    ) -> List[FinanceListInSchema]:
        pagination_dto = PaginationParamsDTO(**pagination.model_dump())
        finance = await self.use_case.list_finance(pagination_dto)
        return [FinanceListInSchema.model_validate(user) for user in finance]

    async def list_finance_out_flow(
        self, pagination: PaginationParamsBaseSchema
    ) -> List[FinanceOutFlowOutSchema]:
        pagination_dto = PaginationParamsDTO(**pagination.model_dump())
        finance = await self.use_case.list_finance_out_flow(pagination_dto)
        return [FinanceOutFlowOutSchema.model_validate(user) for user in finance]

    async def get_finance_out_flow(self, outflow_id: UUID) -> FinanceOutFlowOutSchema:
        finance_case = await self.use_case.get_finance_out_flow(outflow_id)
        return FinanceOutFlowOutSchema.model_validate(finance_case)

    async def updated_finance_out_flow(
        self, outflow_id: UUID, outflow: UpdatedFinanceOutFlowSchema
    ) -> UpdatedFinanceOutFlowOutSchema:
        finance_dto = UpdatedFinanceOutFlowSchema(**outflow.model_dump())
        finance_case = await self.use_case.updated_finance_out_flow(
            outflow_id, finance_dto
        )
        return UpdatedFinanceOutFlowOutSchema.model_validate(finance_case)

    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdSchema:
        finance_case = await self.use_case.get_finance(finance_id)
        return FinanceOutByIdSchema.model_validate(finance_case)

    async def update_finance(
        self, finance_id: UUID, finance: FinanceBaseSchema
    ) -> FinanceOutSchema:
        finance_dto = UpdateFinanceBaseDto(**finance.model_dump())
        finance_case = await self.use_case.update_finance(finance_id, finance_dto)
        return FinanceOutSchema.model_validate(finance_case)

    async def add_finance_outflow(
        self, outflow: FinanceOutFlowBaseSchema
    ) -> FinanceOutFlowOutSchema:
        finance_dto = FinanceOutFlowBaseDto(**outflow.model_dump())
        finance_case = await self.use_case.add_finance_outflow(finance_dto)
        return FinanceOutFlowOutSchema.model_validate(finance_case)

    async def delete_finance(self, finance_id: UUID) -> None:
        await self.use_case.delete_finance(finance_id)
