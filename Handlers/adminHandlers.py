"""Хендлеры для админ-панели."""

from Database.crud import get_all_users

from Utils.admin import CheckAdminFilter

from Keyboards.adminPanelKeyboards import il_adminPanel

from States.states import SendMessageAllUsers

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F


            
router = Router()

            ###   Хендлеры   ###
@router.message(Command('admin'), CheckAdminFilter())
async def admin_panel(message: Message):
    """Обработчик команды /admin."""
    await message.answer('Выберите функцию:', reply_markup=il_adminPanel)

            ###   Состояния   ###
@router.callback_query(F.data == 'admin_panel_main', CheckAdminFilter())
async def sendMessageCallback_getMessage(callback_query: CallbackQuery, state: FSMContext):
    """Начало состояния отправки сообщения всем пользователям - получение."""
    await state.set_state(SendMessageAllUsers.message_collection)
    await callback_query.message.answer(
        'Введите сообщения для отправки всем пользователям (текст, файлы).\n'
        'Для отправки введите /send.'
    )
    await state.update_data(messages=[])

@router.message(Command('send'), CheckAdminFilter(), SendMessageAllUsers.message_collection)
async def sendMessageCallback_sendMessage(message: Message, state: FSMContext):
    """Завершение состояние отправки сообщения всем пользователям - отправка."""
    data = await state.get_data()
    messages_to_send = data.get('messages', [])
    if not messages_to_send:
        await message.answer(
            'Нет сообщений для отправки.\n\n'
            'Введите сообщения (текст, файлы) или /cancel для выхода:'
        )
        return
    all_users = await get_all_users()
    if not all_users:
        await message.answer('Нет подходящих пользователей для отправки сообщений.')
        await state.clear()
        return
    await message.answer(f'Отправка сообщений {len(all_users)} пользователям...')
    await state.clear()
    success_count = 0
    fail_count = 0
    for user in all_users:
        try:
            for msg in messages_to_send:
                if msg['type'] == 'text':
                    await message.bot.send_message(
                        chat_id=user.tg_id,
                        text=msg['content']
                    )
                elif msg['type'] == 'photo':
                    await message.bot.send_photo(
                        chat_id=user.tg_id,
                        photo=msg['content'],
                        caption=msg.get('caption')
                    )
                elif msg['type'] == 'video':
                    await message.bot.send_video(
                        chat_id=user.tg_id,
                        video=msg['content'],
                        caption=msg.get('caption')
                    )
                elif msg['type'] == 'document':
                    await message.bot.send_document(
                        chat_id=user.tg_id,
                        document=msg['content'],
                        caption=msg.get('caption')
                    )
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f'Не удлось отправить сообщениею пользователю {user.tg_id}.\nОшибка: {e}')
    await message.answer(
        f'Отпралено успешно: {success_count} пользователей.\n'
        f'Отправка не удалась: {fail_count} пользователей.'
    )    
    await state.clear()