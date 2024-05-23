from telegram.ext import MessageHandler, CommandHandler, filters
from wolf_assistant.config.telegram_bot import application
from wolf_assistant.handlers.command_handlers import start_reply
from wolf_assistant.handlers.message_handlers import chatgpt_reply
from wolf_assistant.handlers.audio_handlers import audio_reply
from wolf_assistant.handlers.video_note_handlers import video_note_reply
from wolf_assistant.handlers.image_file_handlers import image_file_reply
from wolf_assistant.handlers.video_file_handlers import video_file_reply

# Регистрация обработчиков команд
start_handler = CommandHandler("start", start_reply)
application.add_handler(start_handler)

# Регистрация обработчика текстовых сообщений
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply)
application.add_handler(message_handler)

# Регистрация обработчика аудио сообщений
audio_handler = MessageHandler(filters.VOICE, audio_reply)
application.add_handler(audio_handler)

# Регистрация обработчика видео сообщений
video_note_handler = MessageHandler(filters.VIDEO_NOTE, video_note_reply)
application.add_handler(video_note_handler)

# Регистрация обработчика изображений
photo_handler = MessageHandler(filters.PHOTO, image_file_reply)
application.add_handler(photo_handler)

# Регистрация обработчика видео
video_handler = MessageHandler(filters.VIDEO, video_file_reply)
application.add_handler(video_handler)

# Запуск бота
application.run_polling()
