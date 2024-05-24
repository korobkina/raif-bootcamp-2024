import os

from dotenv import load_dotenv
from wolf_assistant.backend.mongo_logger import MongoConfig

load_dotenv()

ENV = os.getenv("ENV")
MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")


def get_mongo_conf() -> MongoConfig:
    if ENV == "DEV":
        return MongoConfig(
            uri="mongodb://localhost:27017",
            db_name="telegram_bot",
            username="admin",
            password="admin_password"
        )
    else:
        return MongoConfig(
            uri="mongodb://159.65.124.137:27017",
            db_name="telegram_bot",
            username=MONGO_INITDB_ROOT_USERNAME,
            password=MONGO_INITDB_ROOT_PASSWORD
        )
