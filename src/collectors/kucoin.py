import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient
from src.database import DBManager

class KucoinCollector:
    def __init__(self, db: DBManager):
        self.db = db

    async def handle_msg(self, msg):
        if msg['topic'] == '/market/ticker:BTC-USDT':
            price = float(msg["data"]['price'])
            await self.db.set_redis("kucoin", {"price": price})

    async def start(self):
        client = WsToken()
        ws_client = await KucoinWsClient.create(None, client, self.handle_msg, private=False)
        await ws_client.subscribe('/market/ticker:BTC-USDT')
        while True:
            await asyncio.sleep(3600)