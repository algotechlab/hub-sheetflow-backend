from abc import ABC, abstractmethod

from src.core.domain.dtos.finance import FinanceBaseDto, FinanceOutDto


class FinanceRepositoriesInterface(ABC):
    @abstractmethod
    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto: ...
