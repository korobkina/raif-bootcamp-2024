"""Message Hanndler."""

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.clients.openai_client import generate_response, prepare_prompt, check_tokens_length


async def chatgpt_reply(update: Update, context: CallbackContext) -> None:
    """Source Text reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """
    if update.message and update.message.text:
        text: str = update.message.text
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {text}, Context: {context}")

    prompt: str = prepare_prompt(input_text=text, input_format="text")
    
    if check_tokens_length(prompt=prompt):
        reply = generate_response(prompt)
    else:
        reply = "Please split your query, number of tokens is too large"
    
    logger.debug(f"Reply: {reply}")
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
