from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from services.whisper import transcribe_audio
from services.analyzer import analyze_text
from services.balance import get_balance
from aiogram.enums import ParseMode
from utils.promts import (
    PROMT_1, PROMT_2,
    PROMT_3, PROMT_4
    )
from utils.logging import logger
from models import SessionLocal, UserData
from services.video_processing import extract_audio_from_video


# Создаем роутер
router = Router()


def split_message(text: str, max_length: int = 4096) -> list[str]:
    """Разделяет сообщение на части, сохраняя правильную разметку HTML."""
    parts = []
    while len(text) > 0:
        if len(text) <= max_length:
            parts.append(text)
            break
        part = text[:max_length]
        last_newline = part.rfind('\n')  # Ищем последний перенос строки
        if last_newline == -1:
            # Если переносов строки нет, разбиваем по последнему пробелу
            last_space = part.rfind(' ')
            if last_space == -1:
                # Если пробелов нет, разбиваем по max_length
                parts.append(part)
                text = text[max_length:]
            else:
                parts.append(text[:last_space])
                text = text[last_space + 1:]
        else:
            parts.append(text[:last_newline])
            text = text[last_newline + 1:]
    return parts


# Создаем клавиатуру с кнопкой "Запросить баланс"
def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Запросить баланс")]  # Обычная кнопка
        ],
        resize_keyboard=True  # Автоматически подгоняет размер кнопок
    )
    return keyboard


# Обновляем обработчик команды /start, чтобы показывать клавиатуру
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "Привет! Отправь мне аудиофайл в формате mp3."
        " Я сделаю транскрибацию и потом предложу тебе "
        "сценарий для обработки.",
        reply_markup=get_reply_keyboard()  # Показываем клавиатуру
    )


# Добавляем обработчик для кнопки "Запросить баланс"
@router.message(F.text == "Запросить баланс")
async def handle_balance_button(message: Message):
    """Обработчик для кнопки 'Запросить баланс'."""
    balance = get_balance()
    if balance is None:
        await message.answer(
            "Не удалось получить баланс. Проверьте ключ API."
        )
        return
    await message.answer(
        f"<b>Текущий баланс:</b> <u>{balance} руб.</u>"
        )


# Создаем inline кнопки для выбора сценария анализа
def get_analysis_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Квалификация", callback_data="qualification")],
        [InlineKeyboardButton(
            text="Проигрыш", callback_data="loss")],
        [InlineKeyboardButton(
            text="Общий анализ звонка", callback_data="general_analysis")],
        [InlineKeyboardButton(
            text="Проигрыш2(тест)", callback_data="loss2")],

    ])
    return keyboard


# Создаем inline кнопку "Показать транскрибацию"
def get_transcription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Показать транскрибацию", callback_data="show_transcription"
        )]
    ])
    return keyboard


# Обработчик команды /balance
@router.message(Command("balance"))
async def handle_balance(message: Message):
    """Обработчик команды для запроса текущего баланса."""
    balance = get_balance()
    if balance is None:
        await message.answer(
            "Не удалось получить баланс. Проверьте ключ API."
        )
        return
    await message.answer(f"Текущий баланс: {balance} руб.")


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
        await message.answer("Скачал файл, идёт транскрибация.")

        # Транскрибация через OpenAI Whisper с временными метками
        transcription = await transcribe_audio(
            "audio.mp3", return_timestamps=True
        )
        if transcription.startswith("Ошибка"):
            logger.error(f"Ошибка транскрибации: {transcription}")
            await message.answer(transcription)
            return

        logger.info("Транскрибация завершена")
        logger.info(f"Длина транскрипции: {len(transcription)} символов")

        # Сохраняем транскрипцию в базе данных
        db = SessionLocal()
        user_data = db.query(UserData).filter(
            UserData.user_id == message.from_user.id
            ).first()
        if user_data:
            user_data.transcription = transcription
        else:
            user_data = UserData(
                user_id=message.from_user.id, transcription=transcription
                )
            db.add(user_data)
        db.commit()
        db.close()

        # Отправляем сообщение с выбором сценария анализа
        await message.answer(
            "Я закончил транскрибацию звонка, ниже ты"
            " можешь найти варинаты анализа, обращай внимание"
            " на актуальность сценария.\n"
            "<u>Выбери сценарий анализа:</u>\n"
            "\n"
            "<b>1. Стандартная квалификация:</b>\n"
            "Этот вариант для фиксации информации в первом"
            " квалификационном звонке с клиентом(Имя, должность,"
            " гпр и так далее)\n"
            "\n"
            "<b>2. Анализ звонка в проигрыше:</b>\n"
            "Этот вариант для фиксации информации в проигрыше"
            " с клиентом и анализ разговора. \n"
            "\n"
            "<b>3. Общий анализ звонка:</b>\n"
            "Этот режимя для резюмирования разговора, если "
            "нужно вытащить основную суть и зафиксировать всё тезисно\n"
            "\n"
            "<b>4. Проигрыш2 (тест)</b>\n"
            "Пока тестовый промт для анализа проигрыша руководителем.",
            reply_markup=get_analysis_keyboard(),
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {e}")
        await message.answer(f"Произошла ошибка при обработке аудио: {e}")


# Обработчик выбора "Квалификация"
@router.callback_query(F.data == "qualification")
async def handle_qualification(callback: CallbackQuery):
    await callback.answer()

    db = SessionLocal()
    user_data = db.query(UserData).filter(
        UserData.user_id == callback.from_user.id
        ).first()
    db.close()

    if not user_data or not user_data.transcription:
        await callback.message.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по первому промту
    prompt = PROMT_1
    analysis = await analyze_text(user_data.transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(analysis)
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(
                f"<b>Анализ текста, квалификация PreSale:</b>\n{part}",
                parse_mode=ParseMode.HTML
                )
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )


# Обработчик выбора "Проигрыш"
@router.callback_query(F.data == "loss")
async def handle_loss(callback: CallbackQuery):
    await callback.answer()

    db = SessionLocal()
    user_data = db.query(UserData).filter(
        UserData.user_id == callback.from_user.id
        ).first()
    db.close()

    if not user_data or not user_data.transcription:
        await callback.message.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по второму промту
    prompt = PROMT_2
    analysis = await analyze_text(user_data.transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(analysis)
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(
                f"<b>Проигрыш:</b>\n{part}",
                parse_mode=ParseMode.HTML
                )
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )


@router.callback_query(F.data == "loss2")
async def handle_loss2(callback: CallbackQuery):
    await callback.answer()

    db = SessionLocal()
    user_data = db.query(UserData).filter(
        UserData.user_id == callback.from_user.id
        ).first()
    db.close()

    if not user_data or not user_data.transcription:
        await callback.message.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по второму промту
    prompt = PROMT_4
    analysis = await analyze_text(user_data.transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(analysis)
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(
                f"<b>Анализ проигрыша(руководитель):</b>\n{part}",
                parse_mode=ParseMode.HTML
                )
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )


# Добавляем новый обработчик для общего анализа звонка
@router.callback_query(F.data == "general_analysis")
async def handle_general_analysis(callback: CallbackQuery):
    await callback.answer()

    db = SessionLocal()
    user_data = db.query(UserData).filter(
        UserData.user_id == callback.from_user.id
        ).first()
    db.close()

    if not user_data or not user_data.transcription:
        await callback.message.answer("Транскрипция не найдена.")
        return

    # Анализ текста через ChatGPT по третьему промту
    prompt = PROMT_3
    analysis = await analyze_text(user_data.transcription, prompt)
    if analysis.startswith("Ошибка"):
        logger.error(f"Ошибка анализа текста: {analysis}")
        await callback.message.answer(
            f"<b>Общий анализ звонка:</b>\n{analysis}",
            parse_mode=ParseMode.HTML
            )
        return

    # Разбиваем анализ на части и отправляем
    analysis_parts = split_message(analysis)
    for part in analysis_parts:
        try:
            await callback.message.answer(f"Общий анализ звонка:\n{part}")
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части анализа: {e}")

    # Добавляем кнопку "Показать транскрибацию"
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы увидеть транскрибацию:",
        reply_markup=get_transcription_keyboard()
    )


# Обработчик кнопки "Показать транскрибацию"
@router.callback_query(F.data == "show_transcription")
async def handle_show_transcription(callback: CallbackQuery):
    await callback.answer()

    db = SessionLocal()
    user_data = db.query(UserData).filter(
        UserData.user_id == callback.from_user.id
        ).first()
    db.close()

    if not user_data or not user_data.transcription:
        await callback.message.answer("Транскрипция не найдена.")
        return

    # Разбиваем транскрибацию на части и отправляем
    transcription_parts = split_message(user_data.transcription)
    for part in transcription_parts:
        try:
            await callback.message.answer(f"Транскрибация:\n{part}")
        except TelegramBadRequest as e:
            logger.error(f"Ошибка при отправке части транскрибации: {e}")
