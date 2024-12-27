import os

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from config import ADMIN_IDS

log_router = Router()

logger = logging.getLogger(__name__)

LOG_FILE_PATH = os.path.join("logs", "bot_logs.log")
ADMIN_IDS = [int(chat_id) for chat_id in ADMIN_IDS.split(",")]


@log_router.message(Command("get_logs"))
async def send_logs(message: types.Message):
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        return

    if not os.path.exists(LOG_FILE_PATH):
        await message.answer("❗ Лог-файл не найден.")
        return

    try:
        log_file = FSInputFile(LOG_FILE_PATH, filename="bot_logs.log")
        await message.answer_document(log_file, caption="📄 Вот последние логи.")
    except Exception as e:
        logger.error(f"Ошибка отправки логов: {e}")
        await message.answer("❗ Произошла ошибка при отправке логов.")