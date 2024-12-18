from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_for_check = State()
    waiting_for_fio = State()
    waiting_for_address = State()
    waiting_for_phone = State()
