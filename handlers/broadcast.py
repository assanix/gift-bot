import asyncio

from aiogram import Router, types
from aiogram.filters import Command
from database import db
from config import ADMIN_IDS
import logging

broadcast_router = Router()
logger = logging.getLogger(__name__)

ADMIN_IDS = [int(chat_id.strip()) for chat_id in ADMIN_IDS.split(",") if chat_id.strip().isdigit()]


BROADCAST_MESSAGE = (
    "🔊Бүгін сағат 20:00-де Арай қыздарыңыз алғашқы тікелей эфирін бастайды‼\n"
    "Бүгінгі эфирде 5.000.000тг ақшалай, 5 Iphone 16 сыйлайтын боламыз😍\n"
    "Құр қалып қоймаңыз‼\n"
    "Эфир басталуына 5 минут   қалды🙌\n"
    "Төмендегі сілтеме арқылы кіріңіз‼‼👇🏻\n"
    "https://start.bizon365.ru/room/156080/be0bbbaa5685\n "
)


async def broadcast_message(bot, text):
    users = await db.orders.find({}).to_list(None)
    success_count, fail_count = 0, 0

    for user in users:
        chat_id = user.get("chat_id")
        if not chat_id:
            continue

        try:
            await bot.send_message(chat_id, text)
            logger.info(f"Сообщение отправлено пользователю {chat_id}")
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            fail_count += 1
            logger.error(f"Ошибка при отправке пользователю {chat_id}: {e}")

    return success_count, fail_count


@broadcast_router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, bot):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("⛔ У вас нет доступа к этой команде.")
        return

    await message.reply("📤 Рассылка началась...")
    success, fail = await broadcast_message(bot, BROADCAST_MESSAGE)
    await message.reply(f"✅ Успешно отправлено: {success}\n❌ Ошибок: {fail}")