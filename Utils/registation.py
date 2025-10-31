"""Функции для регистрации/изменения профиля пользователя."""

from aiogram.types import Message

from Database.crud import get_user_by_tg_id
from Keyboards import inlineKeyboards as ik

async def get_profile_send_reply(message: Message):
    """" Обработчик реплай-кнопки 'Мой профиль' """
    user_tg_id=message.from_user.id 
    user=await get_user_by_tg_id(user_tg_id)
    if user is None: # пользователь не зарегистрирован в боте
        responce_text="Вы ещё не зарегистрированы! Нажмите кнопку ниже, чтобы завершить регистрацию."
        keyboard=ik.il_RegistrationProfileBtn_insideReply
    else: # пользователь зарегистрирован в боте
        responce_text=(
            f"🧑 Ваш профиль: {user.username}\n"
            f"🍀 Ваше счастливое число: {user.lucky_number}"
        )
        keyboard=ik.il_ChangeProfileBtn_insideReply
    await message.answer(responce_text, reply_markup=keyboard)
