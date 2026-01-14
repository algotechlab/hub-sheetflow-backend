import asyncio

from src.infrastructure.workers.workers_sheetflow import (
    FinanceNotificationWorker,
)
from src.infrastructure.workers.workers_sheetflow_out_flow_finance import (
    FinanceOutFlowNotificationWorker,
)


async def main():
    finance_worker = FinanceNotificationWorker()
    finance_out_flow_worker = FinanceOutFlowNotificationWorker()

    await asyncio.gather(
        finance_worker.run(),
        finance_out_flow_worker.run(),
    )


if __name__ == '__main__':
    asyncio.run(main())

# python -m src.infrastructure.workers.main
