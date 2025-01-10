import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config
from handlers import router
from utils.logging import logger


async def main():
    # Инициализация бота
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Инициализация диспетчера
    dp = Dispatcher()
    dp.include_router(router)

    # Запуск бота
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
