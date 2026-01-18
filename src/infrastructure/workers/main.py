import asyncio

from src.core.domain.models import load_all_models
from src.infrastructure.workers.workers_court_deadline import (
    CourtDeadlineNotificationWorker,
)
from src.infrastructure.workers.workers_sheetflow import (
    FinanceNotificationWorker,
)
from src.infrastructure.workers.workers_sheetflow_out_flow_finance import (
    FinanceOutFlowNotificationWorker,
)

# Carrega todos os modelos antes de iniciar os workers
load_all_models()


async def main():
    finance_worker = FinanceNotificationWorker()
    finance_out_flow_worker = FinanceOutFlowNotificationWorker()
    court_deadline_worker = CourtDeadlineNotificationWorker()

    await asyncio.gather(
        finance_worker.run(),
        finance_out_flow_worker.run(),
        court_deadline_worker.run(),
    )


if __name__ == '__main__':
    asyncio.run(main())

# python -m src.infrastructure.workers.main
