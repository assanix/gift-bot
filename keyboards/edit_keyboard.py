from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить чек", callback_data="edit_check"),
         InlineKeyboardButton(text="👤 Изменить ФИО", callback_data="edit_fio")],
        [InlineKeyboardButton(text="🏠 Изменить адрес", callback_data="edit_address"),
         InlineKeyboardButton(text="📞 Изменить телефон", callback_data="edit_phone")]
    ])
