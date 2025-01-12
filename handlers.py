from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
    )
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from services.whisper import transcribe_audio
from services.analyzer import analyze_text
from services.balance import get_balance, calculate_cost
from utils.promts import PROMT_1, PROMT_2
from utils.logging import logger
import asyncio

# Создаем роутер
router = Router()

# Глобальный словарь для хранения данных пользователя
user_data = {}


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


# Создаем inline кнопки для выбора сценария анализа
def get_analysis_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Квалификация", callback_data="qualification")],
        [InlineKeyboardButton(text="Проигрыш", callback_data="loss")]
    ])
    return keyboard


# Создаем inline кнопку "Показать транскрибацию"
def get_transcription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать транскрибацию", callback_data="show_transcription")]
    ])
    return keyboard


# Обработчик команды /start
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Отправь мне аудиофайл в формате mp3.")


# Обработчик команды /balance
@router.message(Command("balance"))
async def handle_balance(message: Message):
    """Обработчик команды для запроса текущего баланса."""
    balance = get_balance()
    if balance is None:
        await message.answer("Не удалось получить баланс. Проверьте ключ API.")
        return
    await message.answer(f"Текущий баланс: {balance} руб.")


# Обработчик аудиофайлов
@router.message(F.audio)
async def handle_audio(message: Message):
    try:
        logger.info(f"Получено аудио от пользователя {message.from_user.id}")

        # Получаем баланс до выполнения операции
        before_balance = get_balance()
        if before_balance is None:
            await message.answer("Не удалось получить баланс. Проверьте ключ API.")
            return

        # Скачиваем аудиофайл
        file_id = message.audio.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        await message.bot.download_file(file_path, "audio.mp3")
        logger.info("Аудиофайл успешно скачан")

        # Транскрибация через OpenAI Whisper с временными метками
        transcription = await transcribe_audio("audio.mp3", return_timestamps=True)
        if transcription.startswith("Ошибка"):
            logger.error(f"Ошибка транскрибации: {transcription}")
            await message.answer(transcription)
            return

        logger.info("Транскрибация завершена")
        logger.info(f"Длина транскрипции: {len(transcription)} символов")

        # Сохраняем транскрипцию в контексте пользователя
        user_data[message.from_user.id] = {"transcription": transcription}

        # Отправляем сообщение с выбором сценария анализа
        await message.answer("Выбери сценарий анализа", reply_markup=get_analysis_keyboard())

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.answer(f"Произошла ошибка при обработке аудио: {e}")


# Обработчик выбора "Квалификация"
@router.callback_query(F.data == "qualification")
async def handle_qualification(callback: CallbackQuery):
    user_id = callback.from_user.id
    transcription = user_data.get(user_id, {}).get("transcription")

    if not transcription:
        await callback.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по первому промту
    prompt = PROMT_1
    analysis = await analyze_text(transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(analysis)
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(f"Анализ текста:\n{part}")
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )

    # Задержка перед выводом баланса
    await asyncio.sleep(5)

    # Получаем баланс после выполнения операции
    after_balance = get_balance()
    if after_balance is None:
        await callback.message.answer("Не удалось получить баланс после операции.")
        return

    # Рассчитываем стоимость операции
    cost = calculate_cost(before_balance, after_balance)

    # Отправляем пользователю текущий баланс и стоимость операции
    await callback.message.answer(
        f"Текущий баланс: {after_balance} руб.\n"
        f"Стоимость операции: {cost} руб."
    )

    await callback.answer()


# Обработчик выбора "Проигрыш"
@router.callback_query(F.data == "loss")
async def handle_loss(callback: CallbackQuery):
    user_id = callback.from_user.id
    transcription = user_data.get(user_id, {}).get("transcription")

    if not transcription:
        await callback.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по второму промту
    prompt = PROMT_2
    analysis = await analyze_text(transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(analysis)
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(f"Анализ текста:\n{part}")
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )

    # Задержка перед выводом баланса
    await asyncio.sleep(5)

    # Получаем баланс после выполнения операции
    after_balance = get_balance()
    if after_balance is None:
        await callback.message.answer("Не удалось получить баланс после операции.")
        return

    # Рассчитываем стоимость операции
    cost = calculate_cost(before_balance, after_balance)

    # Отправляем пользователю текущий баланс и стоимость операции
    await callback.message.answer(
        f"Текущий баланс: {after_balance} руб.\n"
        f"Стоимость операции: {cost} руб."
    )

    await callback.answer()


# Обработчик кнопки "Показать транскрибацию"
@router.callback_query(F.data == "show_transcription")
async def handle_show_transcription(callback: CallbackQuery):
    user_id = callback.from_user.id
    transcription = user_data.get(user_id, {}).get("transcription")

    if not transcription:
        await callback.answer("Транскрипция не найдена.")
        return

    # Отправляем транскрибацию пользователю
    await callback.message.answer(f"Транскрибация:\n{transcription}")
    await callback.answer()
