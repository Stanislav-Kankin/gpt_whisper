from openai import OpenAI
from config import config
from utils.logging import logger
import asyncio
from moviepy.editor import VideoFileClip

client = OpenAI(
    api_key=config.PROXY_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1"
)

# Ограничение на 5 одновременных запросов
semaphore = asyncio.Semaphore(5)


async def extract_audio_from_video(video_path: str, audio_path: str = "extracted_audio.mp3") -> str:
    """
    Извлекает аудио из видеофайла и сохраняет его в формате mp3.
    Возвращает путь к извлеченному аудиофайлу.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        logger.error(f"Ошибка при извлечении аудио из видео: {e}")
        return None


async def transcribe_audio(
        file_path: str,
        language: str = "ru",
        return_timestamps: bool = False
) -> str:
    """
    Отправляет аудиофайл на транскрибацию через OpenAI Whisper API.
    Возвращает транскрипцию или сообщение об ошибке.
    """
    async with semaphore:
        try:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    language=language,
                    response_format="verbose_json" if return_timestamps else "json"
                )
            if return_timestamps:
                # Формируем текст с временными метками
                text_with_timestamps = []
                for segment in transcription.segments:
                    start_time = segment.start
                    end_time = segment.end
                    text = segment.text
                    text_with_timestamps.append(
                        f"[{start_time:.2f}-{end_time:.2f}] {text}"
                    )
                return "\n".join(text_with_timestamps)
            return transcription.text
        except Exception as e:
            logger.error(f"Ошибка при транскрибации: {e}")
            return f"Ошибка при транскрибации: {e}"
