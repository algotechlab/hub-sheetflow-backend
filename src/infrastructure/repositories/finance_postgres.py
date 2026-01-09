from typing import List
from uuid import UUID

from sqlalchemy import Numeric, cast, literal, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.common.pagination import PaginationParamsDTO
from src.core.domain.dtos.finance import (
    FinanceBaseDto,
    FinanceListOutDto,
    FinanceOutByIdDto,
    FinanceOutDto,
    FinanceOutFlowOutDto,
    HistoryFinanceDto,
    UpdatedFinanceOutFlowDto,
    UpdatedFinanceOutFlowOutDto,
    UpdateFinanceBaseDto,
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

    async def list_finance_out_flow(
        self, pagination: PaginationParamsDTO
    ) -> List[FinanceOutFlowOutDto]:
        try:
            query = (
                select(
                    FinanceOutFlowBox.id,
                    FinanceOutFlowBox.description,
                    FinanceOutFlowBox.value,
                    FinanceOutFlowBox.date_flow,
                    FinanceOutFlowBox.installment_numbers,
                    FinanceOutFlowBox.created_at,
                    FinanceOutFlowBox.updated_at,
                )
                .where(FinanceOutFlowBox.is_deleted.__eq__(False))
                .order_by(FinanceOutFlowBox.created_at)
            )

            if pagination.filter_by and pagination.filter_value:
                query = query.filter(
                    getattr(FinanceOutFlowBox, pagination.filter_by).__eq__(
                        pagination.filter_value
                    )
                )
            result = await self.session.execute(query)
            return [
                FinanceOutFlowOutDto.model_validate(row._mapping)
                for row in result.all()
            ]
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def get_finance_out_flow(self, outflow_id: UUID) -> FinanceOutFlowOutDto:
        try:
            query = select(
                FinanceOutFlowBox.id,
                FinanceOutFlowBox.description,
                FinanceOutFlowBox.value,
                FinanceOutFlowBox.date_flow,
                FinanceOutFlowBox.installment_numbers,
                FinanceOutFlowBox.created_at,
                FinanceOutFlowBox.updated_at,
            ).where(
                FinanceOutFlowBox.id.__eq__(outflow_id),
                FinanceOutFlowBox.is_deleted.__eq__(False),
            )

            result = await self.session.execute(query)
            row = result.one_or_none()

            if not row:
                return None

            return FinanceOutFlowOutDto.model_validate(row._mapping)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def updated_finance_out_flow(
        self, outflow_id: UUID, outflow: UpdatedFinanceOutFlowDto
    ) -> UpdatedFinanceOutFlowOutDto:
        try:
            values = outflow.model_dump(
                exclude_unset=True,
                exclude_none=True,
            )
            if not values:
                return None

            stmt = (
                update(FinanceOutFlowBox)
                .where(
                    FinanceOutFlowBox.id.__eq__(outflow_id),
                    FinanceOutFlowBox.is_deleted.is_(False),
                )
                .values(**values)
                .returning(FinanceOutFlowBox)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_finance = result.scalar_one_or_none()

            if not updated_finance:
                return None

            return UpdatedFinanceOutFlowOutDto.model_validate(updated_finance)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdDto:
        try:
            query = select(
                Finance.id,
                Finance.name,
                Finance.date_contract,
                Finance.document,
                Finance.installment_numbers,
                Finance.total,
                Finance.created_at,
                Finance.updated_at,
            ).where(
                Finance.id.__eq__(finance_id),
                Finance.is_deleted.__eq__(False),
            )

            result = await self.session.execute(query)
            row = result.one_or_none()

            if not row:
                return None

            return FinanceOutByIdDto.model_validate(row._mapping)
        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def get_history_finance(self, finance_id: UUID) -> HistoryFinanceDto:
        try:
            installment_value = cast(Finance.total / literal(10), Numeric(10, 2)).label(
                'installment_value'
            )

            total_calculated = cast(
                Finance.installment_numbers * (Finance.total / literal(10)),
                Numeric(10, 2),
            ).label('total_calculated')

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
                    installment_value,
                    total_calculated,
                )
                .where(
                    Finance.id.__eq__(finance_id),
                    Finance.is_deleted.is_(False),
                )
                .order_by(Finance.created_at)
            )

            result = await self.session.execute(query)
            row = result.first()

            return HistoryFinanceDto.model_validate(row._mapping)

        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def update_finance(
        self, finance_id: UUID, finance: UpdateFinanceBaseDto
    ) -> FinanceOutDto | None:
        try:
            values = finance.model_dump(
                exclude_unset=True,
                exclude_none=True,
            )

            if not values:
                return None

            stmt = (
                update(Finance)
                .where(
                    Finance.id.__eq__(finance_id),
                    Finance.is_deleted.is_(False),
                )
                .values(**values)
                .returning(Finance)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_finance = result.scalar_one_or_none()

            if not updated_finance:
                return None

            return FinanceOutDto.model_validate(updated_finance)

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
