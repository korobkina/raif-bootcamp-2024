import time

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.clients.openai_client import generate_file_response
from wolf_assistant.metrics import metrics


async def image_file_reply(update: Update, context: CallbackContext) -> None:
    """Sorce File reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """

    start_time = time.time()

    # Получение объекта File
    if update.message:
        image_file = await context.bot.get_file(update.message.photo[-1].file_id)
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {image_file}")

    # Получение подписи к изображению
    caption = update.message.caption
    logger.debug(f"Caption: {caption}")

    metrics.REQUEST_COUNT.inc()
    metrics.IMAGE_REQUEST_COUNT.inc()

    reply = generate_file_response(url=image_file.file_path, caption=caption)
    logger.debug(f"Reply: {reply}")

    metrics.REQUEST_LATENCY.observe(time.time() - start_time)
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
