from src.core.domain.dtos.finance import FinanceBaseDto, FinanceOutDto
from src.core.domain.service.finance import FinanceService


class FinanceUseCase:
    def __init__(self, finance_service: FinanceService):
        self.finance_service = finance_service

    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto:
        return await self.finance_service.add_finance(finance)
