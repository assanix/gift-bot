import logging
import pytesseract
from PIL import Image
import fitz
import re
import os

from utils.localization import Localization

logger = logging.getLogger(__name__)

async def extract_text_from_file(file_path: str, loc: Localization) -> str:
    if file_path.endswith(".pdf"):
        pdf_document = fitz.open(file_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
        return text
    else:
        raise ValueError(loc.file_error)


async def validate_receipt(file_path: str, loc: Localization) -> dict:
    try:
        extracted_text = await extract_text_from_file(file_path, loc)
        logger.info(f"Извлеченный текст: {extracted_text}")
        lines = extracted_text.splitlines()
        res = {}
        
        for line in lines:
            if "₸" in line:
                amount_line = line.strip()
                logger.info(f"Найдена строка с суммой: {amount_line}")
                res["amount_line"] = amount_line
            if "QR" in line:
                print(line)
                qr_code_line = line.strip()
                res["qr_code_line"] = qr_code_line
                logger.info(f"Найден QR-код: {qr_code_line}")

            # if "amount_line" not in res or not res["amount_line"]:
            #     raise ValueError(loc.error_no_amount_line)

            if "amount_line" in res and "qr_code_line" in res and res["amount_line"] and res["qr_code_line"]:
                return {
                    "valid": True,
                    "amount_line": res["amount_line"],
                    "qr_code_line": res["qr_code_line"],
                }
                
        return {"valid": False, "error": loc.error_no_amount_line}
    except Exception as e:
        logger.error(f"Ошибка валидации чека: {e}")
        return {"valid": False, "error": str(e)}

