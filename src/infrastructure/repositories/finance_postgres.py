from datetime import datetime, timedelta
from decimal import Decimal
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
    FinanceOutFlowByIdDto,
    FinanceOutFlowOutDto,
    HistoryFinanceDto,
    InstallmentOutDto,
    InstallmentUpdateItem,
    UpdatedFinanceInstallNumbersDto,
    UpdatedFinanceInstallNumbersOutDto,
    UpdatedFinanceOutFlowDto,
    UpdatedFinanceOutFlowInstallNumbersDto,
    UpdatedFinanceOutFlowInstallNumbersOutDto,
    UpdatedFinanceOutFlowOutDto,
    UpdateFinanceBaseDto,
)
from src.core.domain.interface.finance import FinanceRepositoriesInterface
from src.core.domain.models.finance import Finance
from src.core.domain.models.financial_outflow_box import FinanceOutFlowBox
from src.core.domain.models.installment_out_flow_payment import (
    InstallmentOutflowPayment,
)
from src.core.domain.models.installment_payment import InstallmentPayment
from src.core.exceptions.custom import DatabaseException


class FinanceRepositoriesPostgres(FinanceRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_finance(
        self,
        finance: FinanceBaseDto,
    ) -> FinanceOutDto:
        try:
            db_finance = Finance(**finance.model_dump())
            self.session.add(db_finance)
            await self.session.flush()

            installment_value = (
                finance.total / Decimal(finance.installment_numbers)
            ).quantize(Decimal('0.01'))

            installments: list[InstallmentPayment] = []

            for number in range(1, finance.installment_numbers + 1):
                due_date = finance.date_contract + timedelta(days=30 * number)

                installment = InstallmentPayment(
                    installment_number=number,
                    value=installment_value,
                    due_date=due_date,
                    finance_id=db_finance.id,
                )

                installments.append(installment)

            self.session.add_all(installments)

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
            await self.session.flush()
            await self.session.refresh(db_finance)

            if finance_outflow.installment_numbers:
                installment_value = (
                    finance_outflow.value / Decimal(finance_outflow.installment_numbers)
                ).quantize(Decimal('0.01'))

                installments: list[InstallmentOutflowPayment] = []

                for number in range(1, finance_outflow.installment_numbers + 1):
                    due_date = finance_outflow.date_flow + timedelta(days=30 * number)

                    installment = InstallmentOutflowPayment(
                        installment_number=number,
                        value=installment_value,
                        due_date=due_date,
                        finance_out_flow_box_id=db_finance.id,
                    )

                    installments.append(installment)

                self.session.add_all(installments)

                await self.session.flush()

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

    async def get_finance_out_flow(
        self, outflow_id: UUID
    ) -> FinanceOutFlowOutDto | None:
        try:
            stmt = (
                select(
                    FinanceOutFlowBox.id,
                    FinanceOutFlowBox.description,
                    FinanceOutFlowBox.value,
                    FinanceOutFlowBox.date_flow,
                    FinanceOutFlowBox.installment_numbers,
                    FinanceOutFlowBox.created_at,
                    FinanceOutFlowBox.updated_at,
                    InstallmentOutflowPayment.installment_number,
                    InstallmentOutflowPayment.paid_at,
                    InstallmentOutflowPayment.due_date,
                    InstallmentOutflowPayment.value,
                    InstallmentOutflowPayment.charged_at,
                )
                .outerjoin(
                    InstallmentOutflowPayment,
                    InstallmentOutflowPayment.finance_out_flow_box_id.__eq__(
                        FinanceOutFlowBox.id
                    ),
                )
                .where(
                    FinanceOutFlowBox.id.__eq__(outflow_id),
                    FinanceOutFlowBox.is_deleted.__eq__(False),
                )
            )

            result = await self.session.execute(stmt)
            rows = result.all()

            if not rows:
                return None

            finance = rows[0]

            installments = [
                InstallmentOutDto(
                    installment_number=row.installment_number,
                    paid_at=row.paid_at,
                    due_date=row.due_date,
                    value=row.value,
                    charged_at=row.charged_at,
                )
                for row in rows
                if row.installment_number is not None
            ]

            return FinanceOutFlowByIdDto(
                id=finance.id,
                created_at=finance.created_at,
                updated_at=finance.updated_at,
                description=finance.description,
                value=finance.value,
                date_flow=finance.date_flow,
                installment_numbers=finance.installment_numbers,
                installments=installments,
            )
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

    async def get_finance(self, finance_id: UUID) -> FinanceOutByIdDto | None:
        try:
            stmt = (
                select(
                    Finance.id,
                    Finance.name,
                    Finance.date_contract,
                    Finance.document,
                    InstallmentPayment.installment_number,
                    InstallmentPayment.paid_at,
                    InstallmentPayment.due_date,
                    InstallmentPayment.value.label('installment_value'),
                    Finance.total,
                )
                .outerjoin(
                    InstallmentPayment, InstallmentPayment.finance_id.__eq__(Finance.id)
                )
                .where(
                    Finance.id.__eq__(finance_id),
                    Finance.is_deleted.__eq__(False),
                    InstallmentPayment.is_deleted.__eq__(False),
                )
            )

            result = await self.session.execute(stmt)
            rows = result.all()

            if not rows:
                return None

            finance = rows[0]

            installments = [
                InstallmentOutDto(
                    installment_number=row.installment_number,
                    paid_at=row.paid_at,
                    due_date=row.due_date,
                    value=row.installment_value,
                )
                for row in rows
                if row.installment_number is not None
            ]

            return FinanceOutByIdDto(
                id=finance.id,
                name=finance.name,
                date_contract=finance.date_contract,
                document=finance.document,
                total=finance.total,
                installments=installments,
            )

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

    async def updated_finance_install_numbers(
        self,
        finance_id: UUID,
        install_numbers: UpdatedFinanceInstallNumbersDto,
    ) -> UpdatedFinanceInstallNumbersOutDto:
        try:
            updated_installments: list[InstallmentUpdateItem] = []
            updated_at: datetime | None = None

            for item in install_numbers.installments:
                stmt = (
                    update(InstallmentPayment)
                    .where(
                        InstallmentPayment.finance_id.__eq__(finance_id),
                        InstallmentPayment.installment_number.__eq__(
                            item.installment_number
                        ),
                        InstallmentPayment.is_deleted.is_(False),
                    )
                    .values(
                        paid_at=datetime.now(),
                    )
                    .returning(
                        InstallmentPayment.id,
                        InstallmentPayment.installment_number,
                        InstallmentPayment.updated_at,
                    )
                )

                result = await self.session.execute(stmt)
                row = result.mappings().one_or_none()

                updated_installments.append(
                    InstallmentUpdateItem(
                        installment_number=row['installment_number'],
                        paid_at=item.paid_at,
                    )
                )

                updated_at = row['updated_at']

            await self.session.commit()

            return UpdatedFinanceInstallNumbersOutDto(
                id=finance_id,
                installments=updated_installments,
                created_at=updated_at,
                updated_at=updated_at,
            )

        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))

    async def updated_finance_out_flow_install_numbers(
        self,
        finance_out_flow_box_id: UUID,
        finance_out_flow: UpdatedFinanceOutFlowInstallNumbersDto,
    ) -> UpdatedFinanceOutFlowInstallNumbersOutDto:
        try:
            updated_installments: list[InstallmentUpdateItem] = []

            for item in finance_out_flow.installments:
                stmt = (
                    update(InstallmentOutflowPayment)
                    .where(
                        InstallmentOutflowPayment.finance_out_flow_box_id.__eq__(
                            finance_out_flow_box_id
                        ),
                        InstallmentOutflowPayment.installment_number.__eq__(
                            item.installment_number
                        ),
                        InstallmentOutflowPayment.is_deleted.is_(False),
                    )
                    .values(
                        paid_at=datetime.now(),
                    )
                    .returning(
                        InstallmentOutflowPayment.id,
                        InstallmentOutflowPayment.installment_number,
                        InstallmentOutflowPayment.created_at,
                        InstallmentOutflowPayment.updated_at,
                    )
                )
                result = await self.session.execute(stmt)
                row = result.mappings().one_or_none()

                updated_installments.append(
                    InstallmentUpdateItem(
                        installment_number=row['installment_number'],
                        paid_at=item.paid_at,
                    ).model_dump()
                )

            await self.session.commit()
            return UpdatedFinanceOutFlowInstallNumbersOutDto(
                id=finance_out_flow_box_id,
                installments=updated_installments,
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )
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
