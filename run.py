import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router

bot = Bot(token=TOKEN) # токен бота импортируйте из config.py, который в свою очередь создайте в той же папке, что и run.py
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')