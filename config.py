import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен бота
    PROXY_API_KEY = os.getenv("PROXY_API_KEY")  # API-ключ OpenAI


config = Config()
