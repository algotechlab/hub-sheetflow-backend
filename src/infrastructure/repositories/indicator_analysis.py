from sqlalchemy import Numeric, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dtos.indicator_analysis import IndicatorAnalysisBaseDto
from src.core.domain.models.finance import Finance
from src.core.domain.models.financial_outflow_box import FinanceOutFlowBox
from src.core.domain.models.groups import Groups
from src.core.domain.models.installment_payment import InstallmentPayment
from src.core.domain.models.mappings_groups import MappingsGroups
from src.core.domain.models.users import User
from src.core.exceptions.custom import DatabaseException


class IndicadorAnalysisRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_summary_indicator_analysis(self) -> IndicatorAnalysisBaseDto | None:
        try:
            # ---------- Core ----------
            total_groups = (
                select(func.count())
                .select_from(Groups)
                .where(Groups.is_deleted.is_(False))
                .scalar_subquery()
            )

            total_users = (
                select(func.count())
                .select_from(User)
                .where(User.is_deleted.is_(False))
                .scalar_subquery()
            )

            total_clients = (
                select(func.count())
                .select_from(MappingsGroups)
                .where(MappingsGroups.is_deleted.is_(False))
                .scalar_subquery()
            )

            # ---------- Financeiro ----------
            total_to_receive = (
                select(func.coalesce(func.sum(Finance.total), 0))
                .where(Finance.is_deleted.is_(False))
                .scalar_subquery()
            )

            total_exit = (
                select(func.coalesce(func.sum(FinanceOutFlowBox.value), 0))
                .where(FinanceOutFlowBox.is_deleted.is_(False))
                .scalar_subquery()
            )

            # ---------- Parcelas ----------
            total_pending_installments = (
                select(func.count())
                .select_from(InstallmentPayment)
                .where(
                    InstallmentPayment.is_deleted.is_(False),
                    InstallmentPayment.paid_at.is_(None),
                )
                .scalar_subquery()
            )

            total_installments = (
                select(func.count())
                .select_from(InstallmentPayment)
                .where(InstallmentPayment.is_deleted.is_(False))
                .scalar_subquery()
            )

            # ---------- KPIs ----------
            average_ticket = cast(
                total_to_receive
                / func.nullif(
                    select(func.count(Finance.id))
                    .where(Finance.is_deleted.is_(False))
                    .scalar_subquery(),
                    0,
                ),
                Numeric,
            )

            exit_percentage = cast(
                (total_exit / func.nullif(total_to_receive, 0)) * 100,
                Numeric,
            )

            default_rate = cast(
                (total_pending_installments / func.nullif(total_installments, 0)) * 100,
                Numeric,
            )

            revenue_per_group = cast(
                total_to_receive / func.nullif(total_groups, 0),
                Numeric,
            )

            # ---------- Query final ----------
            stmt = select(
                # Core
                total_groups.label('total_groups'),
                total_users.label('total_users'),
                total_clients.label('total_clients'),
                # Financeiro
                total_to_receive.label('total_to_receive'),
                total_exit.label('total_exit'),
                (total_to_receive - total_exit).label('net_balance'),
                # Parcelas
                total_pending_installments.label('total_pending_installments'),
                total_installments.label('total_installments'),
                # KPIs
                average_ticket.label('average_ticket'),
                exit_percentage.label('exit_percentage'),
                default_rate.label('default_rate'),
                revenue_per_group.label('revenue_per_group'),
            )

            result = await self.session.execute(stmt)

            if not result:
                return None

            return IndicatorAnalysisBaseDto.model_validate(result.mappings().one())

        except Exception as error:
            await self.session.rollback()
            raise DatabaseException(str(error))
