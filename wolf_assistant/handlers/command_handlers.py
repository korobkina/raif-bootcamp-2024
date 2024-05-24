import json

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from wolf_assistant.metrics import metrics


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Service commands reply
    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """
    reply = """
        *Ассистент Бот для Data Scientists и Аналитиков*

         Привет! Я ваш Ассистент Бот, созданный специально для Data Scientists и аналитиков. Моя цель — помочь вам в вашей повседневной работе, ответить на вопросы и предоставить полезную информацию. Вот некоторые особенности моей работы:

        - *Одно сообщение — один ответ:* Я не удерживаю контекст между сообщениями, поэтому каждое ваше сообщение рассматривается как отдельный запрос.
        - *Интеграция с OpenAI:* Я использую модели OpenAI для генерации ответов на ваши вопросы.

        Не стесняйтесь задавать свои вопросы, и я постараюсь помочь вам максимально эффективно!
        """
    update_obj = json.dumps(update.to_dict(), indent=4)
    reply_update = "*update object*\n\n" + "```json\n" + update_obj + "\n```"  # Dummy message
    if update.message:
        await update.message.reply_text(reply, parse_mode="Markdown")  # перенаправление ответа в Telegram
    else:
        raise AttributeError("update.message is None")
    metrics.CURRENT_USERS.inc()
    metrics.REQUEST_COUNT.inc()

    logger.debug(f"Assistant state Start: {reply_update}, Context: {context}")
    logger.debug(f"Assistant state Start: {reply}, Context: {context}")
