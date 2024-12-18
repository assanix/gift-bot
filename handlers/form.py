import logging
import os

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from config import DEFAULT_SHEET_RANGE
from services.aws_s3 import upload_file_to_s3
from services.google_sheets import append_to_sheet
from states.order_states import OrderStates
from utils.file import get_extension


logger = logging.getLogger(__name__)
form_router = Router()


@form_router.message(F.content_type.in_({"photo", "document"}))
async def handle_check(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} загрузил чек.")
    processing_message = await message.answer("📥 <i>Обработка вашего файла...</i>")

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer("❗ <b>Ошибка:</b> Пожалуйста, отправьте <u>фото</u> или <u>документ</u> с чеком.")
        return

    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    file_unique_id = file_info.file_unique_id
    extension = get_extension(file_path)

    local_file_name = f"{file_unique_id}{extension}"
    local_path = os.path.join("temp", local_file_name)
    os.makedirs("temp", exist_ok=True)

    downloaded_file = await message.bot.download_file(file_info.file_path)

    with open(local_path, "wb") as f:
        f.write(downloaded_file.read())

    logger.info(f"Файл сохранен локально как {local_path}.")

    try:
        s3_url = await upload_file_to_s3(local_path)
        await state.update_data({"check_link": s3_url})
        logger.info(f"Файл успешно загружен в S3: {s3_url}")
    except Exception as e:
        await message.answer("❗ Произошла ошибка при загрузке файла в облако. Попробуйте еще раз.")
        logger.error(f"Ошибка загрузки файла: {e}")

    os.remove(local_path)

    await processing_message.edit_text("✅ Чек сохранен!")
    await message.answer("2/4 Введите, пожалуйста, <b>ваше ФИО</b> 👤:")
    await state.set_state(OrderStates.waiting_for_fio)


@form_router.message(StateFilter(OrderStates.waiting_for_fio))
async def handle_fio(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} ввел ФИО: {message.text.strip()}.")
    await state.update_data({"fio": message.text.strip()})
    await message.answer("🏠 3/4 Введите, пожалуйста, <b>адрес доставки</b> 📍:")
    await state.set_state(OrderStates.waiting_for_address)


@form_router.message(StateFilter(OrderStates.waiting_for_address))
async def handle_address(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} ввел адрес: {message.text.strip()}.")
    await state.update_data({"address": message.text.strip()})
    await message.answer("📞 4/4 Укажите <b>номер телефона</b> ☎️:")
    await state.set_state(OrderStates.waiting_for_phone)


@form_router.message(StateFilter(OrderStates.waiting_for_phone))
async def handle_phone(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} ввел номер телефона: {message.text.strip()}.")
    await state.update_data({"phone": message.text.strip()})

    data = await state.get_data()
    user_id = message.from_user.id
    fio = data.get("fio")
    address = data.get("address")
    phone = data.get("phone")
    check_link = data.get("check_link")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = message.from_user.username

    values = [[str(user_id), fio, address, phone, check_link, current_time, username]]
    # save_data_to_file(values)
    logger.info(f"Данные пользователя {user_id} собраны: {values}")
    process_append_message = await message.answer("✍️ <i>Записываем ваши данные...</i>")
    await append_to_sheet(values, DEFAULT_SHEET_RANGE)
    await process_append_message.delete()

    await message.answer(
        "🎉 <b>Все готово!</b>\n\n"
        "Ваши данные успешно сохранены:\n"
        f"📄 <b>Чек:</b> {check_link}  \n"
        f"👤 <b>ФИО:</b> {fio}\n"
        f"🏠 <b>Адрес:</b> {address}\n"
        f"📞 <b>Телефон:</b> {phone}\n\n"
        "🚀 <i>Мы свяжемся с вами в ближайшее время!</i> 😊\n\n"
        f"🎟 <b>Ваш уникальный номер для розыгрыша:</b> <code>{user_id}</code>\n\n",

        # reply_markup=edit_keyboard()
    )

    await state.clear()
    logger.info(f"Состояние пользователя {user_id} очищено.")
