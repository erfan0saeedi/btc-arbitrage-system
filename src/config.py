import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_URL = os.getenv("MYSQL_URL")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    SYNC_INTERVAL = float(os.getenv("SYNC_INTERVAL", 1))

    @classmethod
    def validate(cls):
        if not cls.MYSQL_URL:
            raise ValueError("MYSQL_URL is required. Please set it in your environment or .env file.")
