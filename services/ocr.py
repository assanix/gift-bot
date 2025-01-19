import logging
import pytesseract
from PIL import Image
import fitz
import re
import os

from utils.localization import Localization

logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = "tesseract"

import cv2
import numpy as np

def preprocess_image(image_path, save_path="processed_image.jpg"):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Изображение не найдено по пути: {image_path}")

    img = deskew(img)

    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.imwrite(save_path, img)
    return save_path

def deskew(image):

    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


async def extract_text_from_file(file_path: str, loc: Localization) -> str:
    """
    Извлекает текст из PDF или изображения. Если текст встроен как изображение, используется OCR.
    """
    if file_path.endswith(".pdf"):
        pdf_document = fitz.open(file_path)
        text = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            page_text = page.get_text()

            if not page_text.strip():
                logger.info(f"Текст не найден на странице {page_num}, выполняем OCR.")
                pix = page.get_pixmap(dpi=300)
                image_path = f"temp_page_{page_num}.png"
                pix.save(image_path)

                preprocessed_image_path = preprocess_image(image_path)
                image = Image.open(preprocessed_image_path)
                page_text = pytesseract.image_to_string(image, lang="rus+eng")

                os.remove(image_path)
                os.remove(preprocessed_image_path)

            text += page_text

        if not text.strip():
            raise ValueError(loc.error_no_amount_line)

        return text

    elif file_path.endswith((".jpg", ".jpeg", ".png")):
        logger.info(f"Извлекаем текст из изображения: {file_path}")
        preprocessed_image_path = preprocess_image(file_path)
        image = Image.open(preprocessed_image_path)
        text = pytesseract.image_to_string(image, lang="rus+eng")
        os.remove(preprocessed_image_path)

        if not text.strip():
            raise ValueError(loc.error_no_amount_line)

        return text

    else:
        raise ValueError(loc.file_error)


async def validate_receipt(file_path: str, loc: Localization) -> dict:
    """
    Проверяет чек, извлекает сумму. Поднимает ошибки, если чек некорректен.
    """
    print(file_path, ": FILE PATH\n")
    try:
        extracted_text = await extract_text_from_file(file_path, loc)
        logger.info(f"Извлеченный текст: {extracted_text}")
        lines = extracted_text.splitlines()
        res = {"qr_code_line": "None"}


        for line in lines:
            normalized_line = line.strip()
            if re.search(r"^\s*\d+(\s*\d{1,3})*\s*[₸тt]\s*$", normalized_line, re.IGNORECASE):
                amount_line = line.strip()
                logger.info(f"Найдена строка с суммой: {amount_line}")
                amount_line = re.sub(r"[tт]", "₸", amount_line, flags=re.IGNORECASE)
                res["amount_line"] = amount_line
            if "QR" in normalized_line:
                res["qr_code_line"] = normalized_line
                
        if "amount_line" not in res or not res["amount_line"]:
            raise ValueError(loc.error_no_amount_line)

        return {
            "valid": True,
            "amount_line": res["amount_line"],
            "qr_code_line": res["qr_code_line"]
        }

    except ValueError as ve:
        logger.info(f"Ошибка проверки чека: {ve}")
        return {
            "valid": False,
            "error": str(ve)
        }
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return {
            "valid": False,
            "error": loc.file_error
        }


