from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states.order_states import OrderStates

callbacks_router = Router()

@callbacks_router.callback_query(F.data.startswith("edit_"))
async def edit_data(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await callback.answer()

    if action == "check":
        await callback.message.answer("📤 Отправьте новый <b>чек</b> в виде фото или документа:")
        await state.set_state(OrderStates.waiting_for_check)

    elif action == "fio":
        await callback.message.answer("👤 Введите новое <b>ФИО</b>:")
        await state.set_state(OrderStates.waiting_for_fio)

    elif action == "address":
        await callback.message.answer("🏠 Введите новый <b>адрес доставки</b>:")
        await state.set_state(OrderStates.waiting_for_address)

    elif action == "phone":
        await callback.message.answer("📞 Введите новый <b>номер телефона</b>:")
        await state.set_state(OrderStates.waiting_for_phone)
