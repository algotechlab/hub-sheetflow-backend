import asyncio
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.logger import logger
from src.core.config.settings import get_settings
from src.core.domain.models.finance import Finance
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

    async def _get_pending_jobs(
        self,
        session: AsyncSession,
    ) -> list[NotificationJobs]:
        today = date.today()

        stmt = (
            select(NotificationJobs)
            .outerjoin(Finance, Finance.id.__eq__(NotificationJobs.finance_id))
            .where(NotificationJobs.executed.is_(False))
            .where(NotificationJobs.date_contract <= today)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def _build_message(job: NotificationJobs) -> str:
        return (
            f'📌 *Alerta Financeiro*\n\n'
            f'Cliente: {job.name}\n'
            f'Valor: R$ {job.amount}\n'
            f'Valor da parcela restante: R$ {job.amount}\n'
            f'⚠️ Realizar cobrança.'
        )

    async def _process_job(
        self,
        session: AsyncSession,
        job: NotificationJobs,
    ) -> None:
        message = self._build_message(job)

        await self.evolution_api.send_message_whatsapp(
            phone_number=self.contact_phone,
            message=message,
        )

        job.executed = True
        session.add(job)
        await session.commit()

        logger.info(f'📨 Job {job.id} enviado para {self.contact_phone}')

    async def _run_cycle(self) -> None:
        async with self.session_factory() as session:
            jobs = await self._get_pending_jobs(session)

            if not jobs:
                return

            for job in jobs:
                try:
                    await self._process_job(session, job)
                except Exception as error:
                    await session.rollback()
                    logger.error(f'❌ Falha ao processar job {job.id}: {error}')

    async def run(self) -> None:
        logger.info('🚀 FinanceNotificationWorker iniciado')

        while self._running:
            try:
                await self._run_cycle()
            except Exception as error:
                logger.exception(f'🔥 Erro crítico no worker financeiro: {error}')

            await asyncio.sleep(self.POLL_INTERVAL)

    async def shutdown(self) -> None:
        logger.info('🛑 Encerrando FinanceNotificationWorker')
        self._running = False
