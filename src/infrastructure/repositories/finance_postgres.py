from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutDto,
    FinanceOutFlowOutDto,
)
from src.core.domain.interface.finance import FinanceRepositoriesInterface
from src.core.domain.models.finance import Finance
from src.core.domain.models.financial_outflow_box import FinanceOutFlowBox
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

    async def add_finance_outflow(
        self, finance_outflow: FinanceOutFlowBox
    ) -> FinanceOutFlowOutDto:
        try:
            db_finance = FinanceOutFlowBox(**finance_outflow.model_dump())
            self.session.add(db_finance)
            await self.session.commit()
            await self.session.refresh(db_finance)
            return FinanceOutFlowOutDto.model_validate(db_finance)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def list_finance(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceListOutDto]:
        try:
            query = (
                select(
                    Finance.id,
                    Finance.name,
                    Finance.date_contract,
                    Finance.document,
                    Finance.installment_numbers,
                    Finance.total,
                    Finance.created_at,
                    Finance.updated_at,
                )
                .where(Finance.is_deleted.__eq__(False))
                .order_by(Finance.created_at)
            )

            if pagination.filter_by and pagination.filter_value:
                query = query.filter(
                    getattr(Finance, pagination.filter_by).__eq__(
                        pagination.filter_value
                    )
                )
            result = await self.session.execute(query)
            return [
                FinanceListOutDto.model_validate(row._mapping) for row in result.all()
            ]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def delete_finance(self, finance_id: UUID) -> bool:
        try:
            stmt = (
                update(Finance)
                .where(Finance.id.__eq__(finance_id), Finance.is_deleted.__eq__(False))
                .values(is_deleted=True)
                .returning(Finance)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_finance = result.scalar_one_or_none()

            return updated_finance is not None
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
