from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

iButtons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Test button 1!', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')],
])

inlineProfile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить профиль', callback_data='change_profile')]
])

inlineHelp = InlineKeyboardMarkup(inline_keyboard=[
    []
])

inlineDice = InlineKeyboardMarkup(inline_keyboard=[
    []
])

inlinePhotoSearch = InlineKeyboardMarkup(inline_keyboard=[
    []
])