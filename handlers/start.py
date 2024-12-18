import logging
from aiogram import types, Dispatcher, Router
from aiogram.filters import Command

logger = logging.getLogger(__name__)
start_router = Router()


async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил команду /start.")
    await message.answer(
        "👋 <b>Добро пожаловать!</b>\n\n"
        "📤 Пожалуйста, отправьте <b>чек</b> в виде <i>фото</i> или <i>документа</i>, "
        "и мы начнем оформление.\n\n"
    )


start_router.message.register(cmd_start, Command("start"))
