from openai import OpenAI
from config import config
from utils.logging import logger
import httpx

# Настройка прокси (если требуется)
proxy_url = "http://134.255.179.138:3128"  # Замените на ваш прокси

# Создаем кастомный транспорт с прокси
transport = httpx.HTTPTransport(proxy=proxy_url)

# Создаем кастомный HTTP-клиент с транспортом
http_client = httpx.Client(transport=transport)

# Инициализация клиента OpenAI с кастомным HTTP-клиентом
client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    http_client=http_client  # Передаем кастомный клиент
)


async def transcribe_audio(file_path: str) -> str:
    """
    Отправляет аудиофайл на транскрибацию через OpenAI Whisper API.
    Возвращает транскрипцию или сообщение об ошибке.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        return transcription.text
    except Exception as e:
        logger.error(f"Ошибка при транскрибации: {e}")
        return f"Ошибка при транскрибации: {e}"
