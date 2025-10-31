"""Функции для админ-контроля."""

from aiogram.types import Message
from aiogram.filters import BaseFilter

from Database.crud import get_user_by_tg_id



async def check_is_admin(message: Message) -> bool:
    """ Проверяет, является ли пользователь администратором."""
    check_user = await get_user_by_tg_id(message.from_user.id)
    if check_user == None:
        return False
    elif check_user.is_admin:
        return True
    
class CheckAdminFilter(BaseFilter):
    """ Класс - Проверяет, является ли пользователь администратором, можно интегрировать как фильтр"""
    async def __call__(self, message: Message) -> bool:
        check_user = await get_user_by_tg_id(message.from_user.id)
        if check_user == None:
            return False
        elif check_user.is_admin:
            return True