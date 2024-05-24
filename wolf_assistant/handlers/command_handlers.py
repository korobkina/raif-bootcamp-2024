import json

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from backend.mongo_logger import MongoLogger


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, mg_logger: MongoLogger) -> None:
    """
    Service commands reply
    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
        mg_logger: MongoLogger object
    """
    reply = """
        *Ассистент Бот для Data Scientists и Аналитиков*

         Привет! Я ваш Ассистент Бот, созданный специально для Data Scientists и аналитиков. Моя цель — помочь вам в вашей повседневной работе, ответить на вопросы и предоставить полезную информацию. Вот некоторые особенности моей работы:

        - *Одно сообщение — один ответ:* Я не удерживаю контекст между сообщениями, поэтому каждое ваше сообщение рассматривается как отдельный запрос.
        - *Интеграция с OpenAI:* Я использую модели OpenAI для генерации ответов на ваши вопросы.

        Не стесняйтесь задавать свои вопросы, и я постараюсь помочь вам максимально эффективно!
        """
    update_obj = json.dumps(update.to_dict(), indent=4)
    dummy_mess = "*update object*\n\n" + "```json\n" + update_obj + "\n```"  # Dummy message
    chat_id = update.message.chat_id
    command = update.message.text
    if update.message:
        logger.debug(f"Input message: {command}, Context: {context}")
        mg_logger.log_message(chat_id, command, command, reply)
        mg_logger.log_user_info(chat_id=update.message.chat_id, user_info=update.to_dict())
        await update.message.reply_text(reply, parse_mode="Markdown")  # перенаправление ответа в Telegram
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Assistant state Start: {dummy_mess}, Context: {context}")
    logger.debug(f"Assistant state Start: {reply}, Context: {context}")
