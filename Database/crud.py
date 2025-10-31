from sqlalchemy import select

from Database.DBModels.users import User
from Database.data import async_session



async def get_user_by_tg_id(tg_id: int) -> User | None:
    """Получить пользователя по Telegram ID из таблицы users"""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()
    
async def create_user_in_users(
    tg_id: int,
    username: str,
    lucky_number: int,
    tg_username: str | None = None,
    tg_first_name: str | None = None,
    tg_last_name: str | None = None,
) -> User:
    """Добавляет нового пользователя в БД в таблицу users"""
    async with async_session() as session:
        new_user = User(
            tg_id=tg_id,
            tg_username=tg_username,
            tg_first_name=tg_first_name,
            tg_last_name=tg_last_name,
            username=username,
            lucky_number=lucky_number,
            is_admin=False
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
    
async def get_all_users() -> list[User]:
    """Получает всех пользователей таблицы users"""
    async with async_session() as session:
        users_list = await session.execute(select(User))
        return users_list.scalars().all()