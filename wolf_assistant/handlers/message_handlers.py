"""Message Hanndler."""
import time
import re

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest

from wolf_assistant.backend.mongo_logger import MongoLogger
from wolf_assistant.clients.openai_client import generate_response, prepare_prompt, check_tokens_length
from wolf_assistant.data.constant_messages import PLEASE_WAIT_MESSAGE
from wolf_assistant.metrics import metrics
from wolf_assistant.utils.escape_markdown_v2 import escape_markdown_v2


async def chatgpt_reply(update: Update, context: CallbackContext,  mg_logger: MongoLogger) -> None:
    """Source Text reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
        mg_logger: MongoLogger object
    """
    start_time = time.time()

    command = "text"
    
    chat_id: str
    if update.message and update.message.chat_id:
        chat_id = update.message.chat_id
    else:
        chat_id = "unknown"

    if update.message and update.message.text:
        text: str = update.message.text
    else:
        mg_logger.log_message(chat_id, command, command, "No text")
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {text}, Context: {context}")

    prompt: str = prepare_prompt(input_text=text, input_format="text")

    wait_message = await update.message.reply_text(PLEASE_WAIT_MESSAGE, parse_mode="MarkdownV2")

    token_flag, number_tokens = check_tokens_length(prompt=prompt)
    if token_flag:
        reply = escape_markdown_v2(generate_response(prompt))
    else:
        reply = "Please split your query, number of tokens is too large"
    
    logger.debug(f"Reply: {reply}")
    
    metrics.REQUEST_COUNT.inc()

    user: str
    if update.message and update.message.from_user:
        user = update.message.from_user.to_dict()
    else:
        user = {"user_unknown": "unknown user"}

    mg_logger.log_message(chat_id, text, command, reply, number_tokens, **user)

    metrics.REQUEST_LATENCY.observe(time.time() - start_time)

    try:
        await wait_message.delete()
        await update.message.reply_text(reply, parse_mode="MarkdownV2")
    except BadRequest as err:
        msg = f"Error: {err}"
        mg_logger.log_error(msg, reply=reply, chat_id=chat_id)
        logger.error(msg)
        await wait_message.delete()
        await update.message.reply_text("Ошибка при парсинге кода в  маркдаун 😔 " 
                                        "\n Попробуйте поменьше участок кода отправить"
                                        "\n Или попробуй скопировать текст и отправить его к себе в сообщения"
                                        "")
        await update.message.reply_text((f"А так вот твое сообщение 😊: \n"
                                         f"{reply}")
                                        )
