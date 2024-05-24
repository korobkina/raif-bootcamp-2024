import json

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from wolf_assistant.backend.mongo_logger import MongoLogger
from wolf_assistant.data.constant_messages import START_MESSAGE_TEMPLATE

from wolf_assistant.metrics import metrics


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, mg_logger: MongoLogger) -> None:
    """
    Service commands reply
    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
        mg_logger: MongoLogger object
    """

    metrics.CURRENT_USERS.inc()
    metrics.REQUEST_COUNT.inc()
    
    user_name: str = "Дорогой друг"
    if update.effective_user:
        user_name = update.effective_user.full_name

    reply = START_MESSAGE_TEMPLATE.format(user_name=user_name)
    update_obj = json.dumps(update.to_dict(), indent=4)
    dummy_mess = "*update object*\n\n" + "```json\n" + update_obj + "\n```"  # Dummy message
    command = update.message.text
    if update.message:
        chat_id = update.message.chat_id
        logger.debug(f"Input message: {command}, Context: {context}")
        mg_logger.log_message(chat_id, command, command, 0, reply)
        mg_logger.log_user_info(chat_id=update.message.chat_id, user_info=update.to_dict())
        await update.message.reply_text(reply, parse_mode="Markdown")  # перенаправление ответа в Telegram
    else:
        msg = "update.message is None"
        mg_logger.log_error(msg)
        raise AttributeError(msg)

    logger.debug(f"Assistant state Start: {dummy_mess}, Context: {context}")
    logger.debug(f"Assistant state Start: {reply}, Context: {context}")
