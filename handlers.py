from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from services.whisper import transcribe_audio
from services.analyzer import analyze_text
from services.balance import check_balance, estimate_cost
from utils.promts import PROMT_1
from utils.logging import logger

# Создаем роутер
router = Router()


def split_message(text: str, max_length: int = 4096) -> list[str]:
    """Разделяет сообщение на части, сохраняя правильную разметку HTML."""
    parts = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end > len(text):
            end = len(text)
        else:
            # Найти ближайший пробел или символ новой строки перед end
            while end > start and text[end] not in (' ', '\n'):
                end -= 1
            if end == start:
                end = start + max_length
        parts.append(text[start:end])
        start = end
    return parts


# Обработчик команды /start
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне аудиофайл в формате mp3.")


# Обработчик аудиофайлов
@router.message(F.audio)
async def handle_audio(message: Message):
    try:
        logger.info(f"Получено аудио от пользователя {message.from_user.id}")

        # Скачиваем аудиофайл
        file_id = message.audio.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        await message.bot.download_file(file_path, "audio.mp3")
        logger.info("Аудиофайл успешно скачан")

        # Транскрибация через OpenAI Whisper
        transcription = await transcribe_audio("audio.mp3")
        if transcription.startswith("Ошибка"):
            logger.error(f"Ошибка транскрибации: {transcription}")
            await message.answer(transcription)
            return

        logger.info("Транскрибация завершена")
        logger.info(f"Длина транскрипции: {len(transcription)} символов")

        # Разбиваем транскрипцию на части
        transcription_parts = split_message(transcription)
        logger.info(f"Транскрипция разбита на {len(transcription_parts)} частей")

        # Отправляем каждую часть отдельным сообщением
        for part in transcription_parts:
            try:
                await message.answer(f"Транскрипция:\n{part}")
            except TelegramBadRequest as e:
                logger.error(f"Ошибка при отправке части транскрипции: {e}")

        # Анализ текста через ChatGPT
        prompt = PROMT_1
        analysis = await analyze_text(transcription, prompt)
        if analysis.startswith("Ошибка"):
            logger.error(f"Ошибка анализа текста: {analysis}")
            await message.answer(analysis)
            return

        logger.info("Анализ текста завершен")
        logger.info(f"Длина анализа: {len(analysis)} символов")

        # Разбиваем анализ на части
        analysis_parts = split_message(analysis)
        logger.info(f"Анализ разбит на {len(analysis_parts)} частей")

        # Отправляем каждую часть отдельным сообщением
        for part in analysis_parts:
            try:
                await message.answer(f"Анализ текста:\n{part}")
            except TelegramBadRequest as e:
                logger.error(f"Ошибка при отправке части анализа: {e}")

        # Оценка стоимости операции
        whisper_cost = estimate_cost(transcription, model="whisper-1")
        analysis_cost = estimate_cost(analysis, model="gpt-4o")
        total_cost = whisper_cost + analysis_cost

        # Проверка баланса
        balance_info = check_balance()
        await message.answer(f"{balance_info}\nСтоимость операции: {total_cost} руб.")

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.answer(f"Произошла ошибка при обработке аудио: {e}")
