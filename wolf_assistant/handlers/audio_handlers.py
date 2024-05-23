"""Audio Handlers."""

from io import BytesIO

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.clients.openai_client import generate_response, generate_transcription


async def audio_reply(update: Update, context: CallbackContext) -> None:
    """Source Audio reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """

    # входящее аудио сообщение
    if update.message and update.message.voice:
        audio_file = await context.bot.get_file(update.message.voice.file_id)
    else:
        raise AttributeError("update.message is None")

    logger.debug(f"Input message: {audio_file.file_path}")

    # конвертация аудио в формат .ogg
    audio_bytes: BytesIO = BytesIO(await audio_file.download_as_bytearray())

    # запрос транскрипции аудио
    transcription: str = generate_transcription(audio_bytes)
    logger.debug(f"Transcription: {transcription}")

    # openai ответ
    reply = generate_response(transcription)
    logger.debug(f"Reply: {reply}")

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
