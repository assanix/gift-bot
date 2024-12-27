import logging

from config import ADMIN_ID
from database import db

ERROR_STORAGE_PATH = "temp/error_files.json"
ERROR_STATUS_PATH = "temp/error_status.json"

logger = logging.getLogger(__name__)


async def save_failed_upload(file_path, chat_id):
    print("SAVING FAILED UPLOAD")
    error_data = {
        "file_path": file_path,
        "chat_id": chat_id,
        "status": "failed",
        "error_notified": False
    }
    try:
        await db.db.failed_uploads.insert_one(error_data)
        logger.info(f"Ошибка загрузки сохранена: {error_data}")
    except Exception as e:
        logger.error(f"Ошибка сохранения в MongoDB: {e}")


async def notify_admin_once(bot, message, resolved=False):
    admin_id = ADMIN_ID

    try:
        error_status = await db.db.error_status.find_one({"type": "upload_status"})

        if not error_status:
            error_status = {"type": "upload_status", "error_notified": False, "resolved_notified": False}
            await db.db.error_status.insert_one(error_status)

        if not error_status["error_notified"] and not resolved:
            await bot.send_message(admin_id, f"<b>Ошибка загрузки в S3</b>: \n"
                                             f"{message}")
            await db.db.error_status.update_one(
                {"type": "upload_status"},
                {"$set": {"error_notified": True, "resolved_notified": False}}
            )
            await db.db.failed_uploads.update_many(
                {"status": "failed", "error_notified": False},
                {"$set": {"error_notified": True}}
            )
        elif not error_status["resolved_notified"] and resolved:
            await bot.send_message(admin_id, "<b>Все файлы успешно загружены в S3.</b> Проблема решена.")
            await db.db.error_status.update_one(
                {"type": "upload_status"},
                {"$set": {"error_notified": False, "resolved_notified": True}}
            )
    except Exception as e:
        logger.error(f"Ошибка уведомления админа: {e}")