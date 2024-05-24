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
    
    user_name: str = "Дорогой друг"
    if update.effective_user:
        user_name = update.effective_user.full_name

    reply = f"""
        *Ассистент "DS Волчица"*

         {user_name}, тебя привествует DS Волчица. Тебе больше не придется разбираться в чужом коде, так как я проинтерпретирую любой код в любом формате (текст, картинка, аудио, видео).
         Жду от тебя кода в сообщении.

        - *Одно сообщение — один ответ:* Я не удерживаю контекст между сообщениями, поэтому каждое твое сообщение рассматривается как отдельный запрос.
        - *Интеграция с OpenAI:* Я использую модели OpenAI для генерации ответов на твои вопросы.

        Не стесняйся задавать свои вопросы, и я постараюсь помочь тебе максимально эффективно!
        """
    update_obj = json.dumps(update.to_dict(), indent=4)
    reply_update = "*update object*\n\n" + "```json\n" + update_obj + "\n```"  # Dummy message
    if update.message:
        await update.message.reply_text(reply, parse_mode="Markdown")  # перенаправление ответа в Telegram
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Assistant state Start: {reply_update}, Context: {context}")
    logger.debug(f"Assistant state Start: {reply}, Context: {context}")
