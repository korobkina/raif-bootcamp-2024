import os

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


__all__ = [
    'OPENAI_API_KEY',
    'TELEGRAM_BOT_TOKEN'
]
