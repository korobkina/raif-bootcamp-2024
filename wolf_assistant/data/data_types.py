import typing

from telegram.ext import CommandHandler, MessageHandler


Handler = typing.Union[CommandHandler, MessageHandler]
