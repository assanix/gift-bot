import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import Localization

start_router = Router()
logger = logging.getLogger(__name__)


def language_selection_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="language_kk"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="language_en")
        ]
    ])


@start_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.answer(
        loc.language_selection_prompt,
        reply_markup=language_selection_keyboard()
    )
    await state.set_state(OrderStates.waiting_for_language)