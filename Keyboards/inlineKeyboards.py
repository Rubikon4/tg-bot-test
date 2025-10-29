from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



iButtons = InlineKeyboardMarkup(inline_keyboard=[ # Пример инлайн-кнопки
    [InlineKeyboardButton(text='Test button 1!', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')],
]) # пример инлайн-кнопки с URL



            ###   Registration   ###     

il_RegistrationProfileBtn_insideReply = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔑 Зарегистрироваться', callback_data='start_registration')]
])

il_ChangeProfileBtn_insideReply = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️ Изменить профиль', callback_data='start_change_profile')]
]) 

            ###   Прочее   ###

inlineHelp = InlineKeyboardMarkup(inline_keyboard=[
    []
])

inlineDice = InlineKeyboardMarkup(inline_keyboard=[
    []
])

inlinePhotoSearch = InlineKeyboardMarkup(inline_keyboard=[
    []
])