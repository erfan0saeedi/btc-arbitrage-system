import asyncio
import logging
from src.database import DBManager
from src.collectors.kucoin import KucoinCollector
from src.collectors.wallex import WallexCollector
from src.processor.sync_worker import SyncWorker
from src.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


async def main():
    Config.validate()
    db = DBManager()

    kucoin = KucoinCollector(db)
    wallex = WallexCollector(db)
    worker = SyncWorker(db)

    await asyncio.gather(
        kucoin.start(),
        wallex.start(),
        worker.start(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user")
