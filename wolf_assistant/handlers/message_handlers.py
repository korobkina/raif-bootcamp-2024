"""Message Hanndler."""

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.backend.mongo_logger import MongoLogger
from wolf_assistant.clients.openai_client import generate_response, prepare_prompt, check_tokens_length


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
    
    if check_tokens_length(prompt=prompt):
        reply = generate_response(prompt)
    else:
        reply = "Please split your query, number of tokens is too large"
    
    logger.debug(f"Reply: {reply}")

    user: str
    if update.message and update.message.from_user:
        user = update.message.from_user
    else:
        user = "unknown user"

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
