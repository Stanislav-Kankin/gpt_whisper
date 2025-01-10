from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.whisper import transcribe_audio
from services.analyzer import analyze_text
from services.balance import check_balance, estimate_cost
from utils.promts import PROMT_1
from utils.message_splitter import split_text  # Импортируем функцию для разбивки текста

# Создаем роутер
router = Router()


# Обработчик команды /start
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне аудиофайл в формате mp3.")


# Обработчик аудиофайлов
@router.message(F.audio)
async def handle_audio(message: Message):
    # Скачиваем аудиофайл
    file_id = message.audio.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path, "audio.mp3")

    # Транскрибация через OpenAI Whisper
    transcription = await transcribe_audio("audio.mp3")
    transcription_parts = split_text(transcription)  # Разбиваем транскрипцию на части
    for part in transcription_parts:
        await message.answer(f"Транскрипция:\n{part}")

    # Анализ текста через ChatGPT
    prompt = PROMT_1
    analysis = await analyze_text(transcription, prompt)
    analysis_parts = split_text(analysis)  # Разбиваем анализ на части
    for part in analysis_parts:
        await message.answer(f"Анализ текста:\n{part}")

    # Оценка стоимости операции
    whisper_cost = estimate_cost(transcription, model="whisper-1")
    analysis_cost = estimate_cost(analysis, model="gpt-3.5-turbo")
    total_cost = whisper_cost + analysis_cost

    # Проверка баланса
    balance_info = check_balance()
    await message.answer(f"{balance_info}\nСтоимость операции: {total_cost} руб.")
