"""Video Handlers."""

import typing
from io import BytesIO

from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from wolf_assistant.clients.openai_client import generate_transcription, generate_video_response
from wolf_assistant.utils.helpers import frames_to_base64


async def video_reply(update: Update, context: CallbackContext, video_type: typing.Literal["note", "file"]) -> None:
    """Sorce Video reply from chatgpt.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """

    video_file: typing.Any
    caption: typing.Optional[str]

    # получение объекта video_file
    if video_type == "note":
        if update.message and update.message.video_note and update.message.video_note.file_id:
            video_file = await context.bot.get_file(update.message.video_note.file_id)
        else:
            raise AttributeError("update.message is None")
        caption = None
    elif video_type == "file":
        if update.message and update.message.video and update.message.video.file_id:
            video_file = await context.bot.get_file(update.message.video.file_id)
        else:
            raise AttributeError("update.message is None")

        caption = update.message.caption if update.message.caption else "No caption"
    else:
        raise AttributeError(f"Unknown video type: {video_type}")

    logger.debug(f"Input message: {video_file}")
    logger.debug(f"Caption: {caption}")

    # конвертация видео в формат .ogg
    video_bytes = BytesIO(await video_file.download_as_bytearray())

    # получение кадров видео
    video_frames: list[bytes] = frames_to_base64(video_file)
    logger.debug(f"Length of video_frames -> {len(video_frames)}")

    # запрос транскрипции аудио
    transcription: str = generate_transcription(video_bytes) if video_bytes else "No transcription"
    logger.debug(f"Transcription: {transcription}")

    # обработка видео openai
    reply: str = generate_video_response(transcription=transcription, video_frames=video_frames, caption=caption)
    logger.debug(f"Reply: {reply}")

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)


async def video_note_reply(update: Update, context: CallbackContext) -> None:
    """Video note reply.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """
    await video_reply(update=update, context=context, video_type="note")


async def video_file_reply(update: Update, context: CallbackContext) -> None:
    """Video file reply.

    Args:
        update (Update): Telegram object represented an incoming update.
        context (ContextTypes.DEFAULT_TYPE): context object
    """
    await video_reply(update=update, context=context, video_type="file")
