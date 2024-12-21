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
from database import connect_to_mongo, close_mongo_connection

logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing bot ...")
    setup_logging()

    await connect_to_mongo()
    logger.info("Connected to MongoDB.")

    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())


    dp.message.middleware(LocalizationMiddleware())
    dp.callback_query.middleware(LocalizationMiddleware())

 
    dp.include_router(start_router)
    dp.include_router(form_router)
    dp.include_router(callbacks_router)
    dp.include_router(language_router)

    logger.info("Starting polling ...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Closing bot and database connections ...")
        await close_mongo_connection()
        await bot.session.close()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    logger.info("Bot launching ...")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
