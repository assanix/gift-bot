import boto3
import os

import logging

from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, AWS_BUCKET_NAME
from database import db
from utils.file import shorten_url
from utils.troubleshoot import save_failed_upload, notify_admin_once

logger = logging.getLogger(__name__)

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )


async def upload_file_to_s3(file_path: str, chat_id: int, bot) -> str:
    s3_client = get_s3_client()
    file_key = f"checks/{os.path.basename(file_path)}"

    try:
        # raise Exception("Искусственная ошибка загрузки в S3")

        s3_client.upload_file(
            file_path,
            AWS_BUCKET_NAME,
            file_key,
            ExtraArgs={'ACL': 'public-read'}
        )

        url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        logger.info(f"Файл загружен: {url}")
        return url


    except Exception as e:
        logger.error(f"Ошибка загрузки файла в S3: {e}")
        existing_error = await db.db.failed_uploads.find_one({"file_path": file_path, "chat_id": chat_id})

        if not existing_error:
            await save_failed_upload(file_path, chat_id)
            await notify_admin_once(bot, f"Ошибка загрузки файла {file_path}: {e}")

        raise e


async def retry_failed_uploads(bot):
    print("retrying failed uploads")
    try:
        errors = await db.db.failed_uploads.find({"status": "failed"}).to_list(length=None)
        print(errors)

        if not errors:
            logger.info("Нет файлов для повторной загрузки.")
            return

        for error in errors:
            file_path = error["file_path"]
            chat_id = error["chat_id"]

            try:
                await upload_file_to_s3(file_path, chat_id, bot)
                await db.db.failed_uploads.update_one(
                    {"_id": error["_id"]},
                    {"$set": {"status": "uploaded"}}
                )
                await bot.send_message(chat_id, "Ваш файл успешно загружен в S3. Пожалуйста, повторно заполните форму.")
            except Exception as e:
                logger.error(f"Повторная загрузка не удалась для {file_path}: {e}")

        # Check if remain errors
        remaining_errors = await db.db.failed_uploads.find({"status": "failed"}).to_list(length=None)
        if not remaining_errors:
            await notify_admin_once(bot, "Все файлы успешно загружены в S3.", resolved=True)

    except Exception as e:
        logger.error(f"Ошибка обработки повторной загрузки: {e}")
