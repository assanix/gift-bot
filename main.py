import asyncio

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from handlers.callbacks import callbacks_router
from handlers.form import form_router
from handlers.start import start_router
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(form_router)
    dp.include_router(callbacks_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot launching ...")
    asyncio.run(main())
