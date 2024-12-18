# main.py

import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import TELEGRAM_TOKEN
from handlers.callbacks import callbacks_router
from handlers.form import form_router
from handlers.start import start_router
from handlers.language import language_router
from middlewares.localization import LocalizationMiddleware
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

async def main():
    setup_logging()
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))  # Исправлено
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем middleware
    dp.message.middleware(LocalizationMiddleware())
    dp.callback_query.middleware(LocalizationMiddleware())

    # Включаем роутеры
    dp.include_router(start_router)
    dp.include_router(form_router)
    dp.include_router(callbacks_router)
    dp.include_router(language_router)  # Включаем роутер языка

    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Bot launching ...")
    asyncio.run(main())
