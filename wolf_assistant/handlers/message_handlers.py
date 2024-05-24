"""Message Hanndler."""

import time

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.clients.openai_client import generate_response
from wolf_assistant.metrics import metrics


async def chatgpt_reply(update: Update, context: CallbackContext) -> None:
    """Source Text reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """
    start_time = time.time()

    if update.message and update.message.text:
        text: str = update.message.text
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {text}, Context: {context}")
    metrics.REQUEST_COUNT.inc()

    reply = generate_response(text)
    logger.debug(f"Reply: {reply}")

    metrics.REQUEST_LATENCY.observe(time.time() - start_time)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
