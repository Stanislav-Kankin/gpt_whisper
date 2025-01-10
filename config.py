import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен бота
    WHISPER_JAX_URL = os.getenv("WHISPER_JAX_URL")  # URL для транскрибации

config = Config()
