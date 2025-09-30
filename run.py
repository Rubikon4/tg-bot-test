import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN) # токен бота импортируйте из config.py, который в свою очередь создайте в той же папке, что и run.py
dp = Dispatcher()

@dp.message(CommandStart())
async def   cmd_start(message: Message):
    await message.answer('Hello! bot is running...')
@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer('This is /help function.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')