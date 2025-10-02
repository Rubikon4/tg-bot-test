from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Test button 1!'), KeyboardButton(text='Test button 2!')],
    [KeyboardButton(text='Another button 3!!!'), KeyboardButton(text='Another button 4!!!')]
], 
    resize_keyboard=True,
    input_field_placeholder='Try buttons'
)