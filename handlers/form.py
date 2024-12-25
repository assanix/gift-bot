import logging
import os
from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from config import DEFAULT_SHEET_RANGE
from services.aws_s3 import upload_file_to_s3
from services.google_sheets import append_to_sheet
from states.order_states import OrderStates
from utils.file import get_extension
from utils.localization import Localization

from database import db

logger = logging.getLogger(__name__)
form_router = Router()

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
    await message.answer(loc.count_of_orders)
    await state.set_state(OrderStates.waiting_for_count_of_orders)



@form_router.message(StateFilter(OrderStates.waiting_for_count_of_orders))
async def handle_count_of_orders(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел количество товаров: {message.text.strip()}.")
    await state.update_data({"count": message.text.strip()})
    await message.answer(loc.fio_request)
    await state.set_state(OrderStates.waiting_for_fio)
    
@form_router.message(StateFilter(OrderStates.waiting_for_fio))
async def handle_fio(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел ФИО: {message.text.strip()}.")
    await state.update_data({"fio": message.text.strip()})
    await message.answer(loc.region_request)
    await state.set_state(OrderStates.waiting_for_region)

@form_router.message(StateFilter(OrderStates.waiting_for_region))
async def handle_region(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел область: {message.text.strip()}.")
    await state.update_data({"region": message.text.strip()})
    await message.answer(loc.city_request)
    await state.set_state(OrderStates.waiting_for_city)

@form_router.message(StateFilter(OrderStates.waiting_for_city))
async def handle_city(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел город: {message.text.strip()}.")
    await state.update_data({"city": message.text.strip()})
    await message.answer(loc.address_request)
    await state.set_state(OrderStates.waiting_for_address)

@form_router.message(StateFilter(OrderStates.waiting_for_address))
async def handle_address(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел адрес: {message.text.strip()}.")
    await state.update_data({"address_detail": message.text.strip()})
    await message.answer(loc.phone_request)
    await state.set_state(OrderStates.waiting_for_phone)



@form_router.message(StateFilter(OrderStates.waiting_for_phone))
async def handle_phone(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел номер телефона: {message.text.strip()}.")
    await state.update_data({"phone": message.text.strip()})

    data = await state.get_data()
    count = await db.orders.count_documents({})
    user_id = str(count + 1).zfill(7)

    fio = data.get("fio")
    address = f"{data.get('region')}, {data.get('city')}, {data.get('address_detail')}"
    phone = data.get("phone")
    check_link = data.get("check_link")
    count_of_orders = data.get("count")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = message.from_user.username or "N/A"

    values = {
        "user_id": user_id,
        "fio": fio,
        "address": address,
        "phone": phone,
        "check_link": check_link,
        "timestamp": current_time,
        "count_of_orders": count_of_orders,
        "username": username
    }

    try:
        await db.orders.insert_one(values)
        logger.info(f"Данные пользователя {user_id} сохранены в базу данных.")
    except Exception as e:
        logger.error(f"Ошибка сохранения данных в базу: {e}")
        await message.answer(loc.database_save_error)
        return

    process_append_message = await message.answer(loc.processing_data_message)

    try:
        await append_to_sheet(values, DEFAULT_SHEET_RANGE)
    except Exception as e:
        logger.error(f"Ошибка при добавлении данных в Google Sheets: {e}")
        await message.answer(loc.google_sheets_error)

    await process_append_message.delete()

    contract_path = os.path.abspath(os.path.join("contracts", "Договор оферты-Қауашық.docx"))

    if os.path.exists(contract_path):
        try:
            contract_file = FSInputFile(contract_path, filename="Договор оферты-Қауашық.docx")
            await message.answer_document(contract_file, caption=loc.contract_sent_message)
            logger.info(f"Файл {contract_path} успешно отправлен пользователю {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Ошибка при отправке файла: {e}")
            await message.answer(loc.file_send_error)
    else:
        logger.error(f"Файл {contract_path} не найден.")
        await message.answer(loc.file_not_found)

    success_msg = loc.success_message.format(
        check_link=check_link,
        fio=fio,
        address=address,
        phone=phone,
        user_id=user_id
    )

    await message.answer(success_msg)

    await state.clear()
    logger.info(f"Состояние пользователя {username} очищено.")
