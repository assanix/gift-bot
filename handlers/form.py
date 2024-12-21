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
from utils.localization import LOCALIZATIONS, Localization
from database import get_database
import uuid

logger = logging.getLogger(__name__)
form_router = Router()

db = get_database()

@form_router.message(F.content_type.in_({"photo", "document"}))
async def handle_check(message: types.Message, state: FSMContext, loc: Localization):
    user_data = await state.get_data()
    logger.info(f"Пользователь {message.from_user.id} загрузил чек.")
    processing_message = await message.answer(loc.processing_file_message)

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer(loc.file_error)
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
        await message.answer(loc.cloud_upload_error)
        logger.error(f"Ошибка загрузки файла: {e}")
        return

    os.remove(local_path)

    await processing_message.edit_text(loc.check_saved_message)
    await message.answer(loc.fio_request)
    await state.set_state(OrderStates.waiting_for_fio)

@form_router.message(StateFilter(OrderStates.waiting_for_phone))
async def handle_phone(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел номер телефона: {message.text.strip()}.")
    await state.update_data({"phone": message.text.strip()})

    data = await state.get_data()
    user_uuid = uuid.uuid4()

    fio = data.get("fio")
    address = f"{data.get('region')}, {data.get('city')}, {data.get('address_detail')}"
    phone = data.get("phone")
    check_link = data.get("check_link")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = message.from_user.username

    values = {
        "user_id": str(user_uuid),
        "fio": fio,
        "address": address,
        "phone": phone,
        "check_link": check_link,
        "timestamp": current_time,
        "username": username
    }

    logger.info(f"Данные пользователя {user_uuid} собраны: {values}")

    try:
        await db.orders.insert_one(values)
        logger.info(f"Данные пользователя {user_uuid} сохранены в базу данных.")
    except Exception as e:
        logger.error(f"Ошибка сохранения данных в базу: {e}")
        await message.answer(loc.db_save_error)
        return

    await append_to_sheet([[
        str(user_uuid), fio, address, phone, check_link, current_time, username
    ]], DEFAULT_SHEET_RANGE)

    success_msg = loc.success_message.format(
        check_link=check_link,
        fio=fio,
        address=address,
        phone=phone,
        user_id=user_uuid
    )
    await message.answer(success_msg)

    await state.clear()
    logger.info(f"Состояние пользователя {username} очищено.")
