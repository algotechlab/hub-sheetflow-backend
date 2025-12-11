from src.core.domain.dtos.finance import FinanceBaseDto, FinanceOutDto
from src.core.domain.interface.finance import FinanceRepositoriesInterface


class FinanceService:
    def __init__(self, finance_repository: FinanceRepositoriesInterface):
        self.finance_repository = finance_repository

    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto:
        return await self.finance_repository.add_finance(finance)
