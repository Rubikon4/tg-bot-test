"""Функции для регистрации и изменения профиля пользователя."""

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Database import crud
from States.states import Registration, ChangeProfile
from Database.crud import get_user_by_tg_id, create_user_in_users, update_user_in_users
from Keyboards import inlineKeyboards as ik

async def get_profile(message: Message):
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