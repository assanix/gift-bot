import logging
import os
from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from services.aws_s3 import upload_file_to_s3
from services.ocr import validate_receipt
from states.order_states import OrderStates
from utils.file import get_extension
from utils.localization import Localization

from database import db

import re

logger = logging.getLogger(__name__)
form_router = Router()


@form_router.message(F.content_type.in_({"photo", "document"}))
async def handle_check(message: types.Message, state: FSMContext, loc: Localization = "ru"):
    logger.info(f"Пользователь {message.from_user.id} загрузил чек.")
    processing_message = await message.answer(loc.processing_file_message)
    bot = message.bot
    chat_id = message.chat.id

    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer(loc.file_error)
        return

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_unique_id = file_info.file_unique_id
    extension = get_extension(file_path)

    local_file_name = f"{file_unique_id}{extension}"
    local_path = os.path.join("temp", local_file_name)
    os.makedirs("temp", exist_ok=True)

    downloaded_file = await bot.download_file(file_path)
    with open(local_path, "wb") as f:
        f.write(downloaded_file.read())

    logger.info(f"Файл сохранен локально как {local_path}.")

    validation_result = await validate_receipt(local_path, loc)
    if not validation_result["valid"]:
        await message.answer(validation_result['error'])
        os.remove(local_path)
        return

    amount_line = validation_result["amount_line"]
    qr_code_line = validation_result["qr_code_line"]
    amount_cleaned = amount_line.replace("₸", "").replace(" ", "").strip()
    
    existing_qr = await db.orders.find_one({"qr_code_line": qr_code_line})
    if existing_qr:
        await message.answer(
            loc.error_check_repeat
        )
        os.remove(local_path)
        return

    try:
        amount = int(amount_cleaned)
        count_of_orders = amount // 7900
        if count_of_orders == 0:
            await message.answer(
                loc.error_minimum_amount.format(minimum=7900)
            )
            os.remove(local_path)
            return
        await message.answer(
            loc.receipt_verified_message.format(amount=amount, count_of_orders=count_of_orders)
        )
    except ValueError:
        await message.answer(
            loc.error_invalid_amount
        )
        logger.error(f"Ошибка преобразования суммы: {amount_cleaned}")
        os.remove(local_path)
        return

    try:
        s3_url = await upload_file_to_s3(local_path, chat_id, bot)
        await state.update_data({
            "check_link": s3_url,
            "count_of_orders": count_of_orders,
            "qr_code_line": qr_code_line  
        })
        logger.info(f"Файл успешно загружен в S3: {s3_url}")
    except Exception as e:
        await message.answer(loc.cloud_upload_error)
        logger.error(f"Ошибка загрузки файла: {e}")
        os.remove(local_path)
        return
    finally:
        os.remove(local_path)

    await processing_message.edit_text(loc.check_saved_message)
    await message.answer(f"{loc.fio_request}\n\n{loc.example_fio}")
    await state.set_state(OrderStates.waiting_for_fio)


@form_router.message(StateFilter(OrderStates.waiting_for_fio))
async def handle_fio(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел ФИО: {message.text.strip()}.")
    await state.update_data({"fio": message.text.strip()})
    await message.answer(f"{loc.region_request}\n\n{loc.example_region}")
    await state.set_state(OrderStates.waiting_for_region)


@form_router.message(StateFilter(OrderStates.waiting_for_region))
async def handle_region(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел область: {message.text.strip()}.")
    await state.update_data({"region": message.text.strip()})
    await message.answer(f"{loc.city_request}\n\n{loc.example_city}")
    await state.set_state(OrderStates.waiting_for_city)


@form_router.message(StateFilter(OrderStates.waiting_for_city))
async def handle_city(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел город: {message.text.strip()}.")
    await state.update_data({"city": message.text.strip()})
    await message.answer(f"{loc.address_request}\n\n{loc.example_address}")
    await state.set_state(OrderStates.waiting_for_address)


@form_router.message(StateFilter(OrderStates.waiting_for_address))
async def handle_address(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел адрес: {message.text.strip()}.")
    await state.update_data({"address_detail": message.text.strip()})
    await message.answer(f"{loc.phone_request}\n\n{loc.example_phone}")
    await state.set_state(OrderStates.waiting_for_phone)


@form_router.message(StateFilter(OrderStates.waiting_for_phone))
async def handle_phone(message: types.Message, state: FSMContext, loc: Localization):
    logger.info(f"Пользователь {message.from_user.id} ввел номер телефона: {message.text.strip()}.")
    await state.update_data({"phone": message.text.strip()})

    data = await state.get_data()
    fio = data.get("fio")
    address = f"{data.get('region')}, {data.get('city')}, {data.get('address_detail')}"
    phone = data.get("phone")
    check_link = data.get("check_link")
    qr_code_line = data.get("qr_code_line")  
    current_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    username = message.from_user.username or "N/A"
    language = data.get("language")
    chat_id = message.chat.id
    
    count_of_orders = data.get("count_of_orders", 1)

    users_id_arr = []

    for _ in range(count_of_orders):
        order_count = await db.orders.count_documents({})
        user_id = str(order_count + 1).zfill(7)
        users_id_arr.append(user_id)

        values = {
            "user_id": user_id,
            "fio": fio,
            "address": address,
            "phone": phone,
            "check_link": check_link,
            "qr_code_line": qr_code_line,
            "timestamp": current_time,
            "count_of_orders": count_of_orders,
            "username": username,
            "chat_id": chat_id,
            "language": language,
        }

        logger.info(f"Сохраняем данные пользователя {user_id} в базу.")
        try:
            await db.orders.insert_one(values)
            logger.info(f"Данные пользователя {user_id} сохранены в базу данных.")
        except Exception as e:
            logger.error(f"Ошибка сохранения данных в базу: {e}")
            await message.answer(loc.database_save_error)
            return

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
        user_id=", ".join(users_id_arr)
    )
    await message.answer(success_msg)
    await state.clear()
    logger.info(f"Состояние пользователя {username} очищено.")