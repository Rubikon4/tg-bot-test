"""Состояния для FSM."""

from aiogram.fsm.state import StatesGroup, State



class Registration(StatesGroup):
    username = State()
    lucky_number = State()

class ChangeProfile(StatesGroup):
    new_username = State()
    new_lucky_number = State()

class SendMessageAllUsers(StatesGroup):
    message_collection = State()