# middlewares/localization.py

import logging
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from utils.localization import LOCALIZATIONS, Localization

logger = logging.getLogger(__name__)

class LocalizationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: FSMContext = data.get('state')
        language = 'ru'  # Язык по умолчанию

        if state:
            user_data = await state.get_data()
            language = user_data.get("language", 'ru')  # Получаем язык из состояния
            if language not in LOCALIZATIONS:
                language = 'ru'  # Если язык не поддерживается, используем русский
        else:
            logger.warning("No state found, using default language 'ru'.")

        loc = LOCALIZATIONS.get(language, LOCALIZATIONS['ru'])
        data['loc'] = loc  # Передаём локализацию в данные обработчика

        logger.debug(f"User language set to: {language}")

        return await handler(event, data)
