import datetime

from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from wolf_assistant.data.data_types import MongoConfig


class MongoLogger:
    def __init__(self, config: MongoConfig):
        self.client = MongoClient(config.uri, username=config.username, password=config.password)
        self.db = self.client[config.db_name]

    def log_event(self, collection_name: str, event_data: dict):
        try:
            collection = self.db[collection_name]
            event_data['timestamp'] = datetime.datetime.utcnow()
            collection.insert_one(event_data)
        except ServerSelectionTimeoutError as err:
            logger.warning(f"No connection to Mongo, Error: {err}")

    def log_message(self, chat_id: int, text: str, command: str, response_text: str):
        log_entry = {
            'chat_id': chat_id,
            'command': command,  # 'start', 'text', 'voice', 'video_note', 'video', 'photo
            'text': text,
            'response_text': response_text,
        }
        self.log_event('messages', log_entry)

    def log_user_info(self, chat_id: int, **kwargs):
        user_entry = {'chat_id': chat_id, **kwargs}
        self.log_event('users', user_entry)
