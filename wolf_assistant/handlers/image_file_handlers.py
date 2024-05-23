from telegram import Update

from wolf_assistant.config.openai_client import client
from wolf_assistant.utils.helpers import image_to_base64


async def image_file_reply(update, context):
    # Получение объекта File
    image_file = await context.bot.get_file(update.message.photo[-1].file_id)
    print("image_file -> ", image_file)

    # Получение подписи к изображению
    caption = update.message.caption
    print("caption -> ", caption)

    # обработка изображения
    description = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": caption,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_file.file_path,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    # ответ
    reply = description.choices[0].message.content.strip()
    print("assistant:", reply)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)


__all__ = [
    'image_file_reply'
]
