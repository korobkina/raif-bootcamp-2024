from telegram import Update
from config.openai_client import client
from config.openai_client import generate_response

async def chatgpt_reply(update: Update, context):
    # текст входящего сообщения
    text = update.message.text

    # ответ
    reply = generate_response(text)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)

    print("user:", text)
    print("assistant:", reply)
