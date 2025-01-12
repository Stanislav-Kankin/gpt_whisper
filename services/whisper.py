from openai import OpenAI
from config import config
from utils.logging import logger

# Инициализация клиента OpenAI с использованием ProxyAPI
client = OpenAI(
    api_key=config.PROXY_API_KEY,  # Ваш ключ ProxyAPI
    base_url="https://api.proxyapi.ru/openai/v1"  # Базовый URL ProxyAPI
)


async def transcribe_audio(file_path: str, language: str = "ru", return_timestamps: bool = False) -> str:
    """
    Отправляет аудиофайл на транскрибацию через OpenAI Whisper API.
    Возвращает транскрипцию или сообщение об ошибке.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language=language,  # Указываем язык, если известен
                response_format="verbose_json" if return_timestamps else "json"
            )
        if return_timestamps:
            # Формируем текст с временными метками
            text_with_timestamps = []
            for segment in transcription.segments:
                start_time = segment.start  # Используем атрибуты объекта
                end_time = segment.end
                text = segment.text
                text_with_timestamps.append(f"[{start_time:.2f}-{end_time:.2f}] {text}")
            return "\n".join(text_with_timestamps)
        return transcription.text
    except Exception as e:
        logger.error(f"Ошибка при транскрибации: {e}")
        return f"Ошибка при транскрибации: {e}"
