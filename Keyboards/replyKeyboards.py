from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🧑 Мой профиль')],
    [KeyboardButton(text='🎲 Бросить дайс'), KeyboardButton(text='🔍 Помощь')]
], 
    resize_keyboard=True,
    input_field_placeholder='Try buttons'
)