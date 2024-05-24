"""Message Hanndler."""

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from backend.mongo_logger import MongoLogger
from wolf_assistant.clients.openai_client import generate_response


async def chatgpt_reply(update: Update, context: CallbackContext,  mg_logger: MongoLogger) -> None:
    """Source Text reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
        mg_logger: MongoLogger object
    """
    command = "text"

    user = update.message.from_user
    chat_id = update.message.chat_id

    if update.message and update.message.text:
        text: str = update.message.text
    else:
        mg_logger.log_message(chat_id, command, command, "No text")
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {text}, Context: {context}")

    reply = generate_response(text)
    logger.debug(f"Reply: {reply}")
    mongo_log = {
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        "command": command,  # "text
        "text": text,
        "reply": reply,
    }
    mg_logger.log_event('messages', mongo_log)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
