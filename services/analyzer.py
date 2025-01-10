from openai import OpenAI
from config import config
from utils.logging import logger

# Инициализация клиента OpenAI с использованием ProxyAPI
client = OpenAI(
    api_key=config.PROXY_API_KEY,  # Ваш ключ ProxyAPI
    base_url="https://api.proxyapi.ru/openai/v1"  # Базовый URL ProxyAPI
)


async def analyze_text(text: str, prompt: str) -> str:
    """
    Анализирует текст с помощью ChatGPT по заданному промту.
    Возвращает результат анализа или сообщение об ошибке.
    """
    try:
        # Формируем запрос к ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Модель ChatGPT
            messages=[
                {"role": "system", "content": prompt},  # Промт для анализа
                {"role": "user", "content": text}  # Текст для анализа
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при анализе текста: {e}")
        return f"Ошибка при анализе текста: {e}"
