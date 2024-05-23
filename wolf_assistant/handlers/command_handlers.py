import json

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # объект обновления

    reply = """
    *Ассистент Бот для Data Scientists и Аналитиков*

     Привет! Я ваш Ассистент Бот, созданный специально для Data Scientists и аналитиков. Моя цель — помочь вам в вашей повседневной работе, ответить на вопросы и предоставить полезную информацию. Вот некоторые особенности моей работы:

    - *Одно сообщение — один ответ:* Я не удерживаю контекст между сообщениями, поэтому каждое ваше сообщение рассматривается как отдельный запрос.
    - *Интеграция с OpenAI:* Я использую модели OpenAI для генерации ответов на ваши вопросы.

    Не стесняйтесь задавать свои вопросы, и я постараюсь помочь вам максимально эффективно!
    """
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply, parse_mode="Markdown")

    print("assistant:", reply)


__all__ = [
    'start_reply'
]
