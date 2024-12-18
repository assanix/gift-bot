from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from ..utils.localization import LOCALIZATIONS

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
async def cmd_language(message: types.Message):
    await message.answer(
        "Please select your preferred language / Выберите язык / Тілді таңдаңыз:",
        reply_markup=language_selection_keyboard()
    )

@language_router.callback_query(F.data.startswith("language_"))
async def process_language_selection(callback: types.CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[1]
    await state.update_data({"language": language})
    await callback.message.answer(LOCALIZATIONS[language].start_message)
    await callback.answer(f"Language set to: {language}")

def edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить чек", callback_data="edit_check"),
         InlineKeyboardButton(text="👤 Изменить ФИО", callback_data="edit_fio")],
        [InlineKeyboardButton(text="🏠 Изменить адрес", callback_data="edit_address"),
         InlineKeyboardButton(text="📞 Изменить телефон", callback_data="edit_phone")]
    ])
