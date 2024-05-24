"""Message Hanndler."""

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest

from wolf_assistant.backend.mongo_logger import MongoLogger
from wolf_assistant.clients.openai_client import generate_response, prepare_prompt, check_tokens_length
import re

SPECIAL_CHAR_REGEX = re.compile(r'([\\_*[\]()~`><&#+\-=|{}.!])')
CODE_BLOCK_REGEX = re.compile(r'(?is)(```\w* *\n)(.*?)(\n``` *\n)')


def escape_markdown_v2(s: str) -> str:
    return SPECIAL_CHAR_REGEX.sub(r'\\\1', s)


def escape_code_blocks(s: str) -> str:
    def replacing_func(m: re.Match) -> str:
        start, code, end = m.groups()
        escaped_code = escape_markdown_v2(code)
        return f'{start}{escaped_code}{end}'

    return CODE_BLOCK_REGEX.sub(replacing_func, s)


async def chatgpt_reply(update: Update, context: CallbackContext,  mg_logger: MongoLogger) -> None:
    """Source Text reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
        mg_logger: MongoLogger object
    """
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

    token_flag, number_tokens = check_tokens_length(prompt=prompt)
    if token_flag:
        reply = generate_response(prompt)
    else:
        reply = "Please split your query, number of tokens is too large"
    
    logger.debug(f"Reply: {reply}")

    user: str
    if update.message and update.message.from_user:
        user = update.message.from_user.to_dict()
    else:
        user = {"user_unknown": "unknown user"}


    mg_logger.log_message(chat_id, text, command, reply, number_tokens, **user)

    # перенаправление ответа в Telegram

    try:
        await update.message.reply_text(reply, parse_mode="Markdown")
    except BadRequest as err:
        logger.error(f"Error: {err}")
        await update.message.reply_text("Ошибка при парсинге кода в  маркдаун 😔 " 
                                        "\n Попробуйте поменьше участок кода отправить"
                                        "\n Или попробуй скопировать текст и отправить его к себе в сообщения"
                                        "")
        await update.message.reply_text((f"А так вот твое сообщение 😊: \n"
                                         f"{reply}")
                                        )
