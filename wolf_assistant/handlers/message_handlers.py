from wolf_assistant.config.openai_client import client, generate_response
from telegram import Update


async def chatgpt_reply(update: Update, context):
    # текст входящего сообщения
    text = update.message.text

    # ответ
    reply = generate_response(text)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)

    print("user:", text)
    print("assistant:", reply)


__all__ = [
    'chatgpt_reply'
]
