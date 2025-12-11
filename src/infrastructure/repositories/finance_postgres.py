from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.finance import FinanceBaseDto, FinanceOutDto
from src.core.domain.interface.finance import FinanceRepositoriesInterface
from src.core.domain.models.finance import Finance
from src.core.exceptions.custom import DatabaseException


class FinanceRepositoriesPostgres(FinanceRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_finance(self, finance: FinanceBaseDto) -> FinanceOutDto:
        try:
            db_finance = Finance(**finance.model_dump())
            self.session.add(db_finance)
            await self.session.commit()
            await self.session.refresh(db_finance)
            return FinanceOutDto.model_validate(db_finance)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
