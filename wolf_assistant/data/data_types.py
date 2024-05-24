import typing
from dataclasses import dataclass

from telegram.ext import CommandHandler, MessageHandler


Handler = typing.Union[CommandHandler, MessageHandler]

@dataclass
class MongoConfig:
    uri: str
    db_name: str
    username: str
    password: str
