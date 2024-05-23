from telegram.ext import Application 
from wolf_assistant.config.tokens import TELEGRAM_BOT_TOKEN 

# Создание экземпляра бота
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()