import asyncio
import datetime
import logging
from sqlalchemy import text
from src.database import DBManager
from src.config import Config

logger = logging.getLogger(__name__)


class SyncWorker:
    def __init__(self, db: DBManager):
        self.db = db

    @staticmethod
    def extract_prices(kucoin_data: dict, wallex_data: dict):
        if not kucoin_data or not wallex_data or not wallex_data.get("bids"):
            return None
        k_price = float(kucoin_data["price"])
        w_price = float(wallex_data["bids"][0][0])
        return k_price, w_price

    async def start(self):
        await asyncio.sleep(5)
        while True:
            try:
                kucoin_data = await self.db.get_redis("kucoin")
                wallex_data = await self.db.get_redis("wallex")
                prices = self.extract_prices(kucoin_data, wallex_data)

                if prices:
                    k_price, w_price = prices
                    async with self.db.engine.begin() as conn:
                        query = text(
                            "INSERT INTO trade.btc_price (time, price_kucoin, price_wallex) "
                            "VALUES (:t, :k, :w)"
                        )
                        await conn.execute(
                            query,
                            {
                                "t": datetime.datetime.now(datetime.timezone.utc),
                                "k": k_price,
                                "w": w_price,
                            },
                        )
                else:
                    logger.warning("Skipping sync: missing kucoin/wallex data in Redis")

                await asyncio.sleep(Config.SYNC_INTERVAL)
            except Exception as exc:
                logger.error("Sync Error: %s", exc)
                await asyncio.sleep(1)
