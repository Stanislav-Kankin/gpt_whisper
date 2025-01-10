from openai import OpenAI
from config import config
from utils.logging import logger

# Инициализация клиента OpenAI с использованием ProxyAPI
client = OpenAI(
    api_key=config.PROXY_API_KEY,  # Ваш ключ ProxyAPI
    base_url="https://api.proxyapi.ru/openai/v1"  # Базовый URL ProxyAPI
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
