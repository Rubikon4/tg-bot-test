from sqlalchemy import select

from Database.users import User
from Database.data import async_session



async def get_user_by_tg_id(tg_id: int) -> User | None:
    """Получить пользователя по Telegram ID из таблицы users"""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()
    
async def create_user_in_users(tg_id: int, username: str, lucky_number: int) -> User:
    """Добавляет нового пользователя в БД в таблицу users"""
    async with async_session() as session:
        new_user = User(
            tg_id=tg_id,
            username=username,
            lucky_number=lucky_number
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
async def update_user_in_users(tg_id: int, new_username:  str, new_lucky_number: int) -> User | None:
    """Обновляет данные пользователя в БД в таблице users"""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id==tg_id)
        )
        check_user = result.scalar_one_or_none()
        if check_user:
            check_user.username=new_username
            check_user.lucky_number=new_lucky_number
            await session.commit()
            await session.refresh(check_user)
            return check_user
        else:
            return None