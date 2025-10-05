from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мой профиль'), KeyboardButton(text='Помощь')],
    [KeyboardButton(text='Бросить дайс'), KeyboardButton(text='Найти фото (в разработке)')]
], 
    resize_keyboard=True,
    input_field_placeholder='Try buttons'
)