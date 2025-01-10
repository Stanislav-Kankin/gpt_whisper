from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.whisper import transcribe_audio

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

    # Отправляем транскрипцию обратно пользователю
    await message.answer(f"Транскрипция:\n{transcription}")
