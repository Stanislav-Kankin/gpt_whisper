import aiohttp
from config import config


async def transcribe_audio(file_path: str) -> str:
    """
    Отправляет аудиофайл на транскрибацию через Hugging Face Spaces (Whisper-JAX).
    Возвращает транскрипцию или сообщение об ошибке.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Чтение аудиофайла
    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Формируем данные для POST-запроса
    data = aiohttp.FormData()
    data.add_field("data", audio_data, filename="audio.mp3", content_type="audio/mpeg")

    # Отправляем POST-запрос
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(config.WHISPER_JAX_URL, headers=headers, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("data", "Транскрипция не найдена")
                else:
                    return f"Ошибка: {response.status}"
        except Exception as e:
            return f"Ошибка при отправке запроса: {e}"