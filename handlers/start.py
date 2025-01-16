import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import Localization
import os

start_router = Router()
logger = logging.getLogger(__name__)

def get_buy_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="САТЫП АЛАМЫН", callback_data="buy_button")]
    ])

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
    
    welcome_photo = types.FSInputFile("static/start_photo.jpg")
    await message.answer_photo(
        photo=welcome_photo,
        caption="<b>👋🏻 Қош келдіңіз, құрметтім!\n"
        "✅ Бұл отандық өнім \"QAUASAQ\" порошогын сатып алуға арналған ТЕЛЕГРАМ БОТ</b>"
    )

    await message.answer(
        "<b>\"ҚАУАШАҚ\" отандық өнімін пайдаланғаныңыз үшін:\n"
        "🔥 80.000.000 -дық - ҮЙ 🏘\n"
        "🔥 2 СУ ЖАҢА КӨЛІК - 🚘🚘\n"
        "🔥 8 Айфон 16 - 📲\n"
        "🔥 20.000.000 - ақшалай сыйлықтар\n"
        "🔥 Апта сайын ақшалай сыйлықтар 😍\n"
        "Және т.б ҚҰНДЫ СЫЙЛЫҚтардың 🎁 иесі атануыңыз мүмкін!\n"
        "\"Қауашақ\" порошогын алу үшін\n"
        "\"САТЫП АЛАМЫН\" кнопкасын басыңыз.</b>",
        reply_markup=get_buy_button()
    )
    
    await state.set_state(OrderStates.waiting_for_start)

@start_router.callback_query(lambda c: c.data == "buy_button")
async def process_buy_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    instruction_photos = [
        types.FSInputFile("static/instruction1.jpg"),
        types.FSInputFile("static/instruction2.jpg"),
        types.FSInputFile("static/instruction3.jpg")
    ]
    
    instruction_text = (
        "⚙ Инструкция:\n"
        "Оплата жасау үшін сілтемеге өтіңіз:\n"
        "https://pay.kaspi.kz/pay/p1nqjjpr\n"
        "⚠ Бұл жерде міндетті түрде ең аз сумма: 7900 теңге болуы керек!\n"
        "2 порошок алсаңыз: 15800 теңге, 10 порошок - 79000 теңге деген сияқты ровно төлем жасайсыз!\n"
        "Қатесіз төлеңіз!\n"
    )
    
    await callback_query.message.answer_photo(
        photo=instruction_photos[0],
        caption=instruction_text
    )
    
    for photo in instruction_photos[1:]:
        await callback_query.message.answer_photo(photo=photo)
    
    await callback_query.message.answer(
        "Тілді таңдаңыз / Выберите язык / Select language:",
        reply_markup=language_selection_keyboard()
    )
    
    await state.set_state(OrderStates.waiting_for_language)