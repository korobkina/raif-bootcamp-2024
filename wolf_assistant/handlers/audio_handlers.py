from telegram import Update
from config.openai_client import client, generate_response, generate_transcription
from io import BytesIO

async def audio_reply(update: Update, context):
    if update.message.voice is None:
        return
    
    # входящее аудио сообщение
    audio_file = await context.bot.get_file(update.message.voice.file_id)

    # конвертация аудио в формат .ogg
    audio_bytes = BytesIO(await audio_file.download_as_bytearray())
    
    # запрос транскрипции аудио
    transcription = generate_transcription(audio_bytes)
    
    # openai ответ
    reply = generate_response(transcription)
    
    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)
    
    print("user:", audio_file.file_path)
    print("transcription:", text)
    print("assistant:", reply)