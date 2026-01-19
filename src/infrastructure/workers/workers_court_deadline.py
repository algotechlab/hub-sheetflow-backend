import asyncio
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config.logger import logger
from src.core.config.settings import get_settings
from src.core.domain.models.court_deadline import CourtDeadline
from src.core.domain.models.notification_court_deadline import NotificationCourtDeadline
from src.infrastructure.database.session import get_session_factory
from src.infrastructure.extenal_apis.evolution_api import EvolutionApi

settings = get_settings()


class CourtDeadlineNotificationWorker:
    POLL_INTERVAL = 60

    def __init__(self) -> None:
        self.session_factory = get_session_factory()
        self.evolution_api = EvolutionApi()
        self.contact_phone = settings.FINANCE_NOTIFICATION_PHONE
        self._running = True

    async def _get_overdue_court_deadlines(
        self,
        session: AsyncSession,
    ) -> list[tuple[UUID, UUID]]:
        today = datetime.now(timezone.utc).date()
        stmt = (
            select(
                CourtDeadline.id,
                CourtDeadline.groups_id,
                CourtDeadline.mappings_groups_id,
            )
            .where(CourtDeadline.charged_at.is_(None))
            .where(CourtDeadline.prazo <= today)
            .where(CourtDeadline.is_deleted.is_(False))
        )
        result = await session.execute(stmt)
        return result.all()

    @staticmethod
    def _build_message(
        court_deadline: CourtDeadline,
    ) -> str:
        return (
            f'📌 *Alerta de Vencimento de Prazo Judicial*\n\n'
            f'Nome: {court_deadline.name}\n'
            f'Contato: {court_deadline.contato}\n'
            f'Documento: {court_deadline.document}\n'
            f'Prazo a vencer hoje: {court_deadline.prazo}\n\n'
            f'⚠️ Prazo vencido. Realizar ação notificação.'
        )

    async def _process_court_deadline(
        self,
        court_deadline_id: UUID,
        groups_id: UUID,
        mappings_groups_id: UUID,
    ) -> None:
        async with self.session_factory() as session:
            try:
                court_deadline = await session.get(
                    CourtDeadline,
                    court_deadline_id,
                )

                if not court_deadline:
                    logger.warning(
                        '⚠️ Prazo judicial não encontrado',
                        extra={
                            'court_deadline_id': court_deadline_id,
                            'groups_id': groups_id,
                        },
                    )
                    return

                exists_stmt = (
                    select(NotificationCourtDeadline.id)
                    .where(
                        NotificationCourtDeadline.groups_id.__eq__(groups_id),
                        NotificationCourtDeadline.mappings_groups_id.__eq__(
                            mappings_groups_id
                        ),
                    )
                    .where(NotificationCourtDeadline.executed.is_(False))
                )

                exists = await session.execute(exists_stmt)
                if exists.scalar():
                    return

                job = NotificationCourtDeadline(
                    type='COURT_DEADLINE_DUE_ALERT',
                    name=f'Prazo Judicial {court_deadline.name}',
                    contato=court_deadline.contato,
                    document=court_deadline.document,
                    prazo=court_deadline.prazo,
                    groups_id=groups_id,
                    mappings_groups_id=court_deadline.mappings_groups_id,
                )

                session.add(job)
                await session.flush()

                message = self._build_message(court_deadline)

                await self.evolution_api.send_message_whatsapp(
                    phone_number=self.contact_phone,
                    message=message,
                )

                court_deadline.charged_at = datetime.now(tz=timezone.utc)
                job.executed = True

                await session.commit()

                logger.info(
                    '📨 Cobrança de saída enviada com sucesso',
                    extra={
                        'court_deadline_id': court_deadline_id,
                        'groups_id': groups_id,
                    },
                )

            except Exception:
                await session.rollback()
                logger.exception(
                    '❌ Erro ao processar prazo judicial',
                    extra={
                        'court_deadline_id': court_deadline_id,
                        'groups_id': groups_id,
                    },
                )

    async def _run_cycle(self) -> None:
        async with self.session_factory() as session:
            overdue_court_deadlines = await self._get_overdue_court_deadlines(session)

        if not overdue_court_deadlines:
            return

        for court_deadline_id, groups_id, mappings_groups_id in overdue_court_deadlines:
            await self._process_court_deadline(
                court_deadline_id=court_deadline_id,
                groups_id=groups_id,
                mappings_groups_id=mappings_groups_id,
            )

    async def run(self) -> None:
        logger.info('🚀 CourtDeadlineNotificationWorker iniciado')

        while self._running:
            try:
                await self._run_cycle()
            except Exception:
                logger.exception('🔥 Erro crítico no worker prazo judicial')

            await asyncio.sleep(self.POLL_INTERVAL)

    async def shutdown(self) -> None:
        logger.info('🛑 Encerrando CourtDeadlineNotificationWorker')
        self._running = False
