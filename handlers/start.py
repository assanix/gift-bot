# handlers/start.py

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import Localization, LOCALIZATIONS

start_router = Router()

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
    await message.answer(
        loc.language_selection_prompt,
        reply_markup=language_selection_keyboard()
    )
    # Устанавливаем состояние ожидания выбора языка
    await state.set_state(OrderStates.waiting_for_language)
