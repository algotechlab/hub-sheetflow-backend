import asyncio
from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.logger import logger
from src.core.config.settings import get_settings
from src.core.domain.models.financial_outflow_box import FinanceOutFlowBox
from src.core.domain.models.installment_out_flow_payment import (
    InstallmentOutflowPayment,
)
from src.core.domain.models.notification_jobs_out_flow import NotificationJobsOutFlow
from src.infrastructure.database.session import get_session_factory
from src.infrastructure.extenal_apis.evolution_api import EvolutionApi

settings = get_settings()


class FinanceOutFlowNotificationWorker:
    POLL_INTERVAL = 60

    def __init__(self) -> None:
        self.session_factory = get_session_factory()
        self.evolution_api = EvolutionApi()
        self.contact_phone = settings.FINANCE_NOTIFICATION_PHONE
        self._running = True

    async def _get_overdue_installments(
        self,
        session: AsyncSession,
    ) -> list[tuple[UUID, UUID]]:
        stmt = (
            select(
                InstallmentOutflowPayment.id,
                InstallmentOutflowPayment.finance_out_flow_box_id,
            )
            .where(InstallmentOutflowPayment.paid_at.is_(None))
            .where(InstallmentOutflowPayment.charged_at.is_(None))
            .where(InstallmentOutflowPayment.due_date <= date.today())
        )

        result = await session.execute(stmt)
        return result.all()

    @staticmethod
    def _build_message(
        finance_out_flow_box: FinanceOutFlowBox,
        installment: InstallmentOutflowPayment,
    ) -> str:
        return (
            f'📌 *Alerta Financeiro*\n\n'
            f'Cliente: {finance_out_flow_box.description}\n'
            f'Data de vencimento: {installment.due_date}\n'
            f'Valor da parcela: R$ {installment.value}\n\n'
            f'⚠️ Parcela vencida. Realizar cobrança.'
        )

    async def _process_installment(
        self,
        installment_id: UUID,
        finance_out_flow_box_id: UUID,
    ) -> None:
        async with self.session_factory() as session:
            try:
                installment = await session.get(
                    InstallmentOutflowPayment,
                    installment_id,
                )
                finance_out_flow_box = await session.get(
                    FinanceOutFlowBox,
                    finance_out_flow_box_id,
                )

                if not installment or not finance_out_flow_box:
                    logger.warning(
                        '⚠️ Financeiro de saída ou parcela não encontrados',
                        extra={
                            'installment_id': installment_id,
                            'finance_out_flow_box_id': finance_out_flow_box_id,
                        },
                    )
                    return

                exists_stmt = (
                    select(NotificationJobsOutFlow.id)
                    .where(
                        NotificationJobsOutFlow.finance_out_flow_box_id.__eq__(
                            finance_out_flow_box_id
                        )
                    )
                    .where(
                        NotificationJobsOutFlow.installment_numbers.__eq__(
                            installment.installment_number
                        )
                    )
                    .where(NotificationJobsOutFlow.executed.is_(False))
                )

                exists = await session.execute(exists_stmt)
                if exists.scalar():
                    return

                job = NotificationJobsOutFlow(
                    type='OUTFLOW_INSTALLMENT_DUE_ALERT',
                    name=f'Cobrança {finance_out_flow_box.description}',
                    date_flow=finance_out_flow_box.date_flow,
                    value=installment.value,
                    installment_numbers=installment.installment_number,
                    finance_out_flow_box_id=finance_out_flow_box_id,
                )

                session.add(job)
                await session.flush()

                message = self._build_message(finance_out_flow_box, installment)

                await self.evolution_api.send_message_whatsapp(
                    phone_number=self.contact_phone,
                    message=message,
                )

                installment.charged_at = datetime.now(tz=timezone.utc)
                job.executed = True

                await session.commit()

                logger.info(
                    '📨 Cobrança de saída enviada com sucesso',
                    extra={
                        'finance_out_flow_box_id': finance_out_flow_box_id,
                        'installment': installment.installment_number,
                        'amount': str(installment.value),
                    },
                )

            except Exception:
                await session.rollback()
                logger.exception(
                    '❌ Erro ao processar parcela de saída',
                    extra={
                        'installment_id': installment_id,
                        'finance_out_flow_box_id': finance_out_flow_box_id,
                    },
                )

    async def _run_cycle(self) -> None:
        async with self.session_factory() as session:
            overdue_installments = await self._get_overdue_installments(session)

        if not overdue_installments:
            return

        for installment_id, finance_out_flow_box_id in overdue_installments:
            await self._process_installment(
                installment_id=installment_id,
                finance_out_flow_box_id=finance_out_flow_box_id,
            )

    async def run(self) -> None:
        logger.info('🚀 FinanceOutFlowNotificationWorker iniciado')

        while self._running:
            try:
                await self._run_cycle()
            except Exception:
                logger.exception('🔥 Erro crítico no worker financeiro')

            await asyncio.sleep(self.POLL_INTERVAL)

    async def shutdown(self) -> None:
        logger.info('🛑 Encerrando FinanceOutFlowNotificationWorker')
        self._running = False
