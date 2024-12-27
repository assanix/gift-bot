from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates

from utils.localization import Localization, LOCALIZATIONS

from database import db
import aiofiles
from openpyxl import Workbook

from config import USERS

excel_router = Router()
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from openpyxl import Workbook
from aiogram.types import FSInputFile  # Import FSInputFile instead of InputFile

excel_router = Router()


@excel_router.message(Command("get_excel"))
async def cmd_get_excel(message: types.Message, state: FSMContext, loc: Localization):
    if message.from_user.id in [int(_) for _ in USERS.split(",")]:
        items = await db.orders.find().to_list(length=None)
        # Create Excel file
        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"

        # Add headers
        headers = ["user_id", "fio", "address", "phone", "orders_count", "check_link", "timestamp", "username",
                   "chat_id", "language"]
        ws.append(headers)

        # Fill data
        for item in items:
            ws.append([
                item.get("user_id", ""),
                item.get("fio", ""),
                item.get("address", ""),
                item.get("phone", ""),
                item.get("count_of_orders", ""),
                item.get("check_link", ""),
                item.get("timestamp", ""),
                item.get("username", ""),
                item.get("chat_id", ""),
                item.get("language", "")
            ])

        # Save file
        file_path = "orders.xlsx"
        wb.save(file_path)

        # Send file to user using FSInputFile instead of InputFile
        document = FSInputFile(file_path, filename="orders.xlsx")
        await message.answer_document(document)