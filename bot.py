import os
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from dotenv import load_dotenv
import aiohttp
from bs4 import BeautifulSoup

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота с использованием DefaultBotProperties
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Устанавливаем HTML-разметку по умолчанию
)
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
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "audio.mp3")

    # Транскрибация через Hugging Face Spaces (Whisper-JAX)
    transcription = await transcribe_audio("audio.mp3")

    # Отправляем транскрипцию обратно пользователю
    await message.answer(f"Транскрипция:\n{transcription}")

# Функция для транскрибации аудио через Hugging Face Spaces
async def transcribe_audio(file_path):
    url = "https://sanchit-gandhi-whisper-jax.hf.space/run/predict"  # URL Hugging Face Spaces
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
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("data", "Транскрипция не найдена")
            else:
                return f"Ошибка: {response.status}"

# Запуск бота
async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())