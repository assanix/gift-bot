# handlers/callbacks.py

import logging
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates
from utils.localization import LOCALIZATIONS, Localization

callbacks_router = Router()

@callbacks_router.callback_query(F.data.startswith("edit_"))
async def edit_data(callback: types.CallbackQuery, state: FSMContext, loc: Localization):
    user_data = await state.get_data()
    language = user_data.get("language", "ru")  # Язык по умолчанию, но уже установлен через middleware

    action = callback.data.split("_")[1]
    await callback.answer()

    if action == "check":
        await callback.message.answer(loc.check_request)
        await state.set_state(OrderStates.waiting_for_check)

    elif action == "fio":
        await callback.message.answer(loc.fio_request)
        await state.set_state(OrderStates.waiting_for_fio)

    elif action == "address":
        await callback.message.answer(loc.region_request)
        await state.set_state(OrderStates.waiting_for_region)

    elif action == "phone":
        await callback.message.answer(loc.phone_request)
        await state.set_state(OrderStates.waiting_for_phone)