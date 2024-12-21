import json
import logging
import mimetypes
import os

import pyshorteners

from config import BITLY_API_KEY

logger = logging.getLogger(__name__)
DATA_FILE = "user_data.json"

def save_data_to_file(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logger.info(f"Данные сохранены в файл {DATA_FILE}.")


def get_extension(file_path: str) -> str:
    extension = os.path.splitext(file_path)[-1]
    if not extension:
        extension = mimetypes.guess_extension(file_path) or ".bin"
    return extension


def shorten_url(url: str) -> str:
    shortener = pyshorteners.Shortener(api_key=BITLY_API_KEY)
    return shortener.bitly.short(url)
