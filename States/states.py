from aiogram.fsm.state import StatesGroup, State

class Registation(StatesGroup):
    name = State()
    lucky_number = State()