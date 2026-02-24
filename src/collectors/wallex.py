import asyncio
import logging
import httpx
from src.database import DBManager

logger = logging.getLogger(__name__)


class WallexCollector:
    def __init__(self, db: DBManager):
        self.db = db
        self.url = "https://api.wallex.ir/v1/depth?symbol=BTCUSDT"

    @staticmethod
    def parse_orderbook(payload: dict):
        result = payload.get("result", {})
        asks = [[item["price"], item["quantity"]] for item in result.get("ask", [])]
        bids = [[item["price"], item["quantity"]] for item in result.get("bid", [])]
        return asks, bids

    async def start(self):
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(self.url, timeout=2.0)
                    response.raise_for_status()
                    data = response.json()

                    asks, bids = self.parse_orderbook(data)

                    if asks and bids:
                        await self.db.set_redis("wallex", {"asks": asks, "bids": bids})
                    else:
                        logger.warning("Wallex returned empty orderbook")

                    await asyncio.sleep(0.5)
                except Exception as exc:
                    logger.error("Wallex Error: %s", exc)
                    await asyncio.sleep(1)
