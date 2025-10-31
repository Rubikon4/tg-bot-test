from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



inlineLibrarySections = InlineKeyboardMarkup(inline_keyboard=[ # Меню секций библиотеки
    [InlineKeyboardButton(text='1️⃣ Секция', callback_data='library_section_1')],
    [InlineKeyboardButton(text='2️⃣ Секция', callback_data='library_section_2')]
])

library_sections = {
    '1': InlineKeyboardMarkup(inline_keyboard=[ # Cекция 1
    [InlineKeyboardButton(text='Интернет', callback_data='lib_internet')],
    [InlineKeyboardButton(text='Биоинтерфейс', callback_data='lib_biointerface')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='lib_main')]
]),
    '2': InlineKeyboardMarkup(inline_keyboard=[ # Cекция 2
    [InlineKeyboardButton(text='Свобода', callback_data='lib_freedom')],
    [InlineKeyboardButton(text='Рабство', callback_data='lib_slavery')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='lib_main')]
])
}