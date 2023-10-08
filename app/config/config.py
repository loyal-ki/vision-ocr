import os
from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseSettings

ROOT = Path(__file__).parent.parent.parent

print(ROOT)


class BaseConfig(BaseSettings):
    # APP
    APP_ENV: str = "local"
    VERSION: str = "0.0.1"
    API_TITLE: str = ""
    REFRESH_COUNT_LIMIT: int = 10

    LOG_DIR = os.path.join(ROOT, "logs")
    LOG_NAME = os.path.join(LOG_DIR, "azure_vision.log")

    # SERVER
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int

    # MOCK SERVER
    MOCK_ON: bool
    PROXY_ON: bool
    PROXY_PORT: int

    # MYSQL
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB_NAME: str
    MYSQL_TEST_DB_NAME: str = "azure_vision_test"

    # SQLALCHEMY
    SQL_ALCHEMY_DATABASE_URI: str = ""
    ASYNC_SQL_ALCHEMY_URI: str = ""

    # REDIS
    REDIS_ON: bool
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_NODES: List[dict] = []

    # RETRY
    RETRY_TIMES = 1

    # LOG
    AZURE_VISION_ERROR = "AZURE_VISION_ERROR"
    AZURE_VISION_INFO = "AZURE_VISION_INFO"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_AUD_CREATE: str = "azure_vision:create"
    JWT_AUD_VERIFY: str = "azure_vision:verify"
    JWT_AUD_RESET: str = "azure_vision:reset"

    # AZURE
    AZURE_VISION_KEY: str = ""
    AZURE_VISION_ENDPOINT: str = ""
    AZURE_VISION_API_ENDPOINT: str = ""
    AZURE_FORM_RECOGNIZER_KEY: str = ""
    AZURE_FORM_RECOGNIZER_ENDPOINT: str = ""


class DevConfig(BaseConfig):
    class Config:
        env_file = os.path.join(ROOT, "conf", "dev.env")


class ProConfig(BaseConfig):
    class Config:
        env_file = os.path.join(ROOT, "conf", "pro.env")


AZURE_VISION_ENV = os.environ.get("azure_vision_env", "dev")

Config = ProConfig() if AZURE_VISION_ENV and AZURE_VISION_ENV.lower() == "pro" else DevConfig()

Config.REDIS_NODES = [
    {
        "host": Config.REDIS_HOST,
        "port": Config.REDIS_PORT,
        "db": Config.REDIS_DB,
        "password": Config.REDIS_PASSWORD,
    }
]


class AppEnv(str, Enum):
    local = "local"
    staging = "staging"
    prod = "production"


# pylint: disable=anomalous-backslash-in-string
BANNER = """
 _____ _____ _____ _____ _____    _____ _____ _____ _____ _____ _____ 
|  _  |__   |  |  | __  |   __|  |  |  |     |   __|     |     |   | |
|     |   __|  |  |    -|   __|  |  |  |-   -|__   |-   -|  |  | | | |
|__|__|_____|_____|__|__|_____|   \___/|_____|_____|_____|_____|_|___|                                                                                                                  
"""
# pylint: disable=anomalous-backslash-in-string
