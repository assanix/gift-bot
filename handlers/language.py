# handlers/language.py
import logging
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from utils.localization import Localization, LOCALIZATIONS
from states.order_states import OrderStates

logger = logging.getLogger(__name__)
language_router = Router()


def language_selection_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="language_kk"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="language_en")
        ]
    ])

@language_router.message(Command("language"))
async def cmd_language(message: types.Message, state: FSMContext, loc: Localization):
    await message.answer(
        loc.language_selection_prompt,
        reply_markup=language_selection_keyboard()
    )

    await state.set_state(OrderStates.waiting_for_language)

@language_router.callback_query(F.data.startswith("language_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext, loc: Localization):
    language = callback.data.split("_")[1]
    await state.update_data({"language": language})
    logger.info(f"User {callback.from_user.id} selected language {language}.")
    confirmation_message = loc.language_set_confirmation.format(language=language.upper())
    await callback.message.edit_text(confirmation_message)
    await callback.answer(f"Language set to: {language.upper()}")

    await state.set_state(OrderStates.waiting_for_start)
    await callback.message.answer(LOCALIZATIONS[language].start_message)