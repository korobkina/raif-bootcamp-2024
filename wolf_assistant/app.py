"""Main script for the Application."""

from loguru import logger
from prometheus_client import start_http_server
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from wolf_assistant.data.data_types import Handler
from wolf_assistant.handlers.audio_handlers import audio_reply
from wolf_assistant.handlers.command_handlers import start_reply
from wolf_assistant.handlers.image_file_handlers import image_file_reply
from wolf_assistant.handlers.message_handlers import chatgpt_reply
from wolf_assistant.handlers.video_handlers import video_file_reply, video_note_reply
from wolf_assistant.settings import TELEGRAM_BOT_TOKEN


APPLICATION = Application.builder().token(TELEGRAM_BOT_TOKEN).build()  # Создание экземпляра бота

HANDLERS: list[Handler] = [
    CommandHandler(command="start", callback=start_reply),  # Регистрация обработчиков команд
    MessageHandler(
        filters=filters.TEXT & ~filters.COMMAND, callback=chatgpt_reply
    ),  # Регистрация обработчика текстовых сообщений
    MessageHandler(filters=filters.VOICE, callback=audio_reply),  # Регистрация обработчика аудио сообщений
    MessageHandler(filters=filters.VIDEO_NOTE, callback=video_note_reply),  # Регистрация обработчика видео сообщений
    MessageHandler(filters=filters.VIDEO, callback=video_file_reply),  # Регистрация обработчика видео
    MessageHandler(filters=filters.PHOTO, callback=image_file_reply),  # Регистрация обработчика изображений
]


# Start up the server to expose the metrics.
start_http_server(8000)  # Expose metrics on port 8000


if __name__ == "__main__":
    logger.debug("Write handlers to application")
    handler: Handler
    for handler in HANDLERS:
        APPLICATION.add_handler(handler)

    logger.debug("Launch bot")
    APPLICATION.run_polling()
