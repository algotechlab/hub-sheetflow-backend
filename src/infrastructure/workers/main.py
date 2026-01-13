import asyncio

from src.infrastructure.workers.workers_sheetflow import FinanceNotificationWorker


async def main():
    worker = FinanceNotificationWorker()
    await worker.run()


if __name__ == '__main__':
    asyncio.run(main())

# python -m src.infrastructure.workers.main
