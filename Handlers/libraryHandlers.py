"""Хендлеры для работы с библиотекой файлов бота."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from Keyboards import libraryKeyboards as lk

from Utils.library import read_file

from Database.crud import get_user_by_tg_id



router = Router()

@router.message(Command('library'))
async def cmd_library(message: Message):
    """Хендлер для команды /library. Предоставляет доступ пользователю к библиотеке файлов"""
    if get_user_by_tg_id(message.from_user.id) is None:
        await message.answer('Cначала нужно зарегистрироваться! Нажми кнопку "🧑 Мой профиль" и следуй инструкциям.')
    else:
        keyboard = lk.inlineLibrarySections
        await message.answer('Добро пожаловать в библиотеку! Выберете секцию:', reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('library_section_'))
async def select_library_section(callback: CallbackQuery):
    """Универсальный хендлер для обработки выбора секций библиотеки"""
    section = callback.data.split('_')[-1]
    keyboard = lk.library_sections.get(section)
    if keyboard:
        await callback.message.edit_text('Выберете тему:', reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('lib_'))
async def select_library_topic(callback: CallbackQuery):
    """Универсальный хендлер для обработки выбора тем в секциях библиотеки"""
    if callback.data == 'lib_main':
            keyboard = lk.inlineLibrarySections
            await callback.message.edit_text('Добро пожаловать в библиотеку! Выберете секцию:', reply_markup=keyboard)
            return
    try:       
        topic = callback.data.split('_')[-1]
        file_path = f'./Library/{topic}.md'
        content = await read_file(file_path)
        await callback.message.edit_text(content) # parse_mode='MarkdownV2'
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {file_path}")
        await callback.message.answer('Документ в данный момент не доступен...')
    except Exception as e:
        print(f"[ERROR] Ошибка при чтении файла {file_path}: {e}")
        await callback.message.answer('Документ в данный момент не доступен...')


