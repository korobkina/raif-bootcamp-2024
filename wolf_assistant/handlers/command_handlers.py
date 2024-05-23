"""Telegram Command Handlers."""

import json

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Service commands reply
    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """

    update_obj = json.dumps(update.to_dict(), indent=4)
    reply = "*update object*\n\n" + "```json\n" + update_obj + "\n```"  # Dummy message
    if update.message:
        await update.message.reply_text(reply, parse_mode="Markdown")  # перенаправление ответа в Telegram
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Assistant: {reply}, Context: {context}")
