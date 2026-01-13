import asyncio
from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.logger import logger
from src.core.config.settings import get_settings
from src.core.domain.models.finance import Finance
from src.core.domain.models.installment_payment import InstallmentPayment
from src.core.domain.models.notification_jobs import NotificationJobs
from src.infrastructure.database.session import get_session_factory
from src.infrastructure.extenal_apis.evolution_api import EvolutionApi

settings = get_settings()


class FinanceNotificationWorker:
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
                InstallmentPayment.id,
                InstallmentPayment.finance_id,
            )
            .where(InstallmentPayment.paid_at.is_(None))
            .where(InstallmentPayment.charged_at.is_(None))
            .where(InstallmentPayment.due_date <= date.today())
        )

        result = await session.execute(stmt)
        return result.all()

    @staticmethod
    def _build_message(
        finance: Finance,
        installment: InstallmentPayment,
    ) -> str:
        return (
            f'📌 *Alerta Financeiro*\n\n'
            f'Cliente: {finance.name}\n'
            f'Parcela: {installment.installment_number}\n'
            f'Valor: R$ {installment.value}\n\n'
            f'⚠️ Parcela vencida. Realizar cobrança.'
        )

    async def _process_installment(
        self,
        installment_id: UUID,
        finance_id: UUID,
    ) -> None:
        async with self.session_factory() as session:
            try:
                installment = await session.get(
                    InstallmentPayment,
                    installment_id,
                )
                finance = await session.get(
                    Finance,
                    finance_id,
                )

                if not installment or not finance:
                    logger.warning(
                        '⚠️ Finance ou parcela não encontrados',
                        extra={
                            'installment_id': installment_id,
                            'finance_id': finance_id,
                        },
                    )
                    return

                exists_stmt = (
                    select(NotificationJobs.id)
                    .where(NotificationJobs.finance_id.__eq__(finance.id))
                    .where(
                        NotificationJobs.installment_numbers.__eq__(
                            installment.installment_number
                        )
                    )
                    .where(NotificationJobs.executed.is_(False))
                )

                exists = await session.execute(exists_stmt)
                if exists.scalar():
                    return

                job = NotificationJobs(
                    type='INSTALLMENT_DUE_ALERT',
                    name=f'Cobrança {finance.name}',
                    date_contract=finance.date_contract,
                    amount=installment.value,
                    installment_numbers=installment.installment_number,
                    finance_id=finance.id,
                )

                session.add(job)
                await session.flush()

                message = self._build_message(finance, installment)

                await self.evolution_api.send_message_whatsapp(
                    phone_number=self.contact_phone,
                    message=message,
                )

                installment.charged_at = datetime.now(tz=timezone.utc)
                job.executed = True

                await session.commit()

                logger.info(
                    '📨 Cobrança enviada com sucesso',
                    extra={
                        'finance_id': finance.id,
                        'installment': installment.installment_number,
                        'amount': str(installment.value),
                    },
                )

            except Exception:
                await session.rollback()
                logger.exception(
                    '❌ Erro ao processar parcela',
                    extra={
                        'installment_id': installment_id,
                        'finance_id': finance_id,
                    },
                )

    async def _run_cycle(self) -> None:
        async with self.session_factory() as session:
            overdue_installments = await self._get_overdue_installments(session)

        if not overdue_installments:
            return

        for installment_id, finance_id in overdue_installments:
            await self._process_installment(
                installment_id=installment_id,
                finance_id=finance_id,
            )

    async def run(self) -> None:
        logger.info('🚀 FinanceNotificationWorker iniciado')

        while self._running:
            try:
                await self._run_cycle()
            except Exception:
                logger.exception('🔥 Erro crítico no worker financeiro')

            await asyncio.sleep(self.POLL_INTERVAL)

    async def shutdown(self) -> None:
        logger.info('🛑 Encerrando FinanceNotificationWorker')
        self._running = False
