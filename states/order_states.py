from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_start = State()
    waiting_for_check = State()
    waiting_for_count_of_orders = State()
    waiting_for_fio = State()
    waiting_for_region = State()
    waiting_for_city = State()
    waiting_for_address = State()
    waiting_for_phone = State()