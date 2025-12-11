from src.application.api.v1.schemas.finance import FinanceBaseSchema, FinanceOutSchema
from src.core.domain.dtos.finance import FinanceBaseDto
from src.core.domain.use_case.finance import FinanceUseCase


class FinanceController:
    def __init__(self, use_case: FinanceUseCase):
        self.use_case = use_case

    async def add_finance(self, finance: FinanceBaseSchema) -> FinanceOutSchema:
        finance_dto = FinanceBaseDto(**finance.model_dump())
        finance_case = await self.use_case.add_finance(finance_dto)
        return FinanceOutSchema.model_validate(finance_case)
