import asyncio

from src.infrastructure.workers.woerkers_sheetflow_out_flow_finance import (
    FinanceOutFlowNotificationWorker,
)
from src.infrastructure.workers.workers_sheetflow import FinanceNotificationWorker


async def main():
    finance_worker = FinanceNotificationWorker()
    finance_out_flow_worker = FinanceOutFlowNotificationWorker()
    await finance_worker.run()
    await finance_out_flow_worker.run()


if __name__ == '__main__':
    asyncio.run(main())

# python -m src.infrastructure.workers.main
