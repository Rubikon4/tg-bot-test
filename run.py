import asyncio
import logging

from aiogram import Bot, Dispatcher
#from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands

from Config.config import TOKEN

from Handlers.handlers import router
from Handlers.libraryHandlers import router as library_router

bot = Bot(token=TOKEN) # Токен бота импортируется из config.py, который в свою очередь создаётся в той же папке, что и run.py
dp = Dispatcher()

#async def set_chat_menu_button(): # Устновка меню команд (встроенная кнопка телеграм в диалоговом окне с ботом).
#    my_сommands = [               # Требуется включить права пользования в BotFFather для каждой команды отдельно.
#        BotCommand(command='start', description='🚀 Старт!'),
#        BotCommand(command='register', description='🧑 Зарегистрироваться или посмотреть свой профиль.'),
#        BotCommand(command='library', description='📚 Библиотека.'),
#        BotCommand(command='help', description='🔍 Помогатор на случай если запутался.')
#    ]    
#    await bot.set_my_commands(commands=my_сommands, scope=BotCommandScopeDefault())
#    await bot.set_chat_menu_button(
#        chat_id=None,
#        menu_button=MenuButtonCommands()
#    )

async def main():
    dp.include_router(library_router)
    dp.include_router(router)
#    await set_chat_menu_button()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nБОТ ОСТАНОВЛЕН.\n')