import boto3
import os

import logging

from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, AWS_BUCKET_NAME
from utils.file import shorten_url

logger = logging.getLogger(__name__)

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )


async def upload_file_to_s3(file_path: str) -> str:
    s3_client = get_s3_client()
    file_key = f"checks/{os.path.basename(file_path)}"

    try:
        s3_client.upload_file(
            file_path,
            AWS_BUCKET_NAME,
            file_key,
            ExtraArgs={'ACL': 'public-read'}
        )

        url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        logger.info(f"Файл загружен: {url}")
        return shorten_url(url)

    except Exception as e:
        logger.error(f"Ошибка загрузки файла в S3: {e}")
        raise e
