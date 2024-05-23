from telegram import Update
from wolf_assistant.config.openai_client import client, generate_transcription
from io import BytesIO
from wolf_assistant.utils.helpers import frames_to_base64

async def video_note_reply(update, context):
    # получение объекта video_file
    video_file = await context.bot.get_file(update.message.video_note.file_id)
    print("video_file -> ", video_file)

    # конвертация видео в формат .ogg
    audio_bytes = BytesIO(await video_file.download_as_bytearray())
    
    # получение кадров видео
    video_frames = frames_to_base64(video_file)
    print("length of video_frames -> ", len(video_frames))

    # запрос транскрипции аудио
    transcription = generate_transcription(audio_bytes) if audio_bytes else "No transcription"
    print("transcription -> ", transcription)

    # обработка видео openai
    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": transcription,
                    },
                    *map(lambda x: {"image": x, "resize": 768}, video_frames[0::300]),
                ],
            },
        ],
        max_tokens=200,
    )

    # ответ
    reply = result.choices[0].message.content.strip()
    print("assistant:", reply)

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply)