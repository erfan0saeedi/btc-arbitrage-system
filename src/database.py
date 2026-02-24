import json
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

class DBManager:
    def __init__(self):
        # Async MySQL Engine
        self.engine = create_async_engine(Config.MYSQL_URL, echo=False)
        # Async Redis
        self.redis = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    async def set_redis(self, key: str, data: dict, expiry: int = 3):
        await self.redis.setex(key, expiry, json.dumps(data))

    async def get_redis(self, key: str):
        data = await self.redis.get(key)
        return json.loads(data) if data else None