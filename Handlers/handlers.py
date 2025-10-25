from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Keyboards import replyKeyboards as rk
from Keyboards import inlineKeyboards as ik

from States.states import Registration, ChangeProfile

from Database.crud import create_user_in_users, update_user_in_users

from Utils.registation import get_profile



router = Router()
    
            ###   Командные хендлеры   ###
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello! bot is running... Type /help for commands list.', reply_markup=rk.rButtons)

@router.message(Command('dice'))
async def roll_dice(message: Message):
    await message.answer_dice()

@router.message(Command('getID'))
async def get_id(message: Message):
    await message.reply(f'Your ID: {message.from_user.id}\nYour name: {message.from_user.first_name}') # reply для ОТВЕТА на сообщение (как функция тг)

@router.message(Command('meme'))
async def get_meme(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMxaN0uaIVb7R4yLWBLZORJ0U3IUVEAAtD7MRueBelKtCJgPakJ0xIBAAMCAAN5AAM2BA',
                               caption='AHAHAHAHAHAHAHH AHAHHAH AHHA haha.....', reply_markup=ik.iButtons)

@router.message(Command('reg'))
async def cmd_register(message: Message):
    await get_profile(message)

            ###   Кнопочные хендлеры на реплай кнопки   ###
@router.message(F.text == '🧑 Мой профиль')
async def profile_button(message: Message):
    await get_profile(message)
        
@router.message(F.text == '🎲 Бросить дайс')
async def roll_dice_button(message: Message):
    await message.answer_dice()

@router.message(F.text == 'Найти фото (в разработке)')
async def say_hello(message: Message):
    await message.answer('Сказал же, что в разработке! Потом появится...')
        
            ###   Смешанные хендлеры (CMD+РеплайКнопки)   ###     
@router.message(Command('help'))
@router.message(F.text == '🔍 Помощь')
async def get_help(message: Message):
    await message.answer(
    '/help to get to get commands list\n'
    '/meme to get funny meme lol\n'
    '/dice to throw dice\n'
    '/getID to get your personal ID\n'
    '/reg to register yourself'
)
            ###   Прочие хендлеры   ###
@router.message(F.photo)                            
async def get_photo(message: Message):
    await message.answer(f'Your Photo_ID: {message.photo[-1].file_id}')

@router.message(F.text == 'Hello')
async def say_hello(message: Message):
    await message.answer('Hello mate!')

            ###   Коллбэки   ###
"""Регистрация"""
@router.callback_query(F.data == 'start_registration')
async def reg_start_step(callback: CallbackQuery, state: FSMContext):
    """Регистрация по инлайн кнопке 'il_RegistrationProfileBtn_insideReply'."""
    await callback.answer()
    await state.set_state(Registration.username)
    await callback.message.answer('Для начала, введи свой никнейм (до 30 символов):')
@router.message(Registration.username)
async def reg_username_step(message: Message, state: FSMContext):
    user_input = message.text
    if len(user_input) > 30:
        await message.answer('❌ Никнейм слишком длинный! Максимум 30 символов. Попробуй снова:')
    elif len(user_input) == 0:
        await message.answer('❌ Никнейм не может быть пустым! Попробуй снова:')
    else:
        await state.update_data(username=message.text)
        await state.set_state(Registration.lucky_number)
        await message.answer(f'Отлично, {message.text}!\nТеперь укажи своё счастливое число:')
@router.message(Registration.lucky_number)
async def reg_luckyNumber_step(message: Message, state: FSMContext):
    try:
        user_input = int(message.text)
        if user_input > 0:
            await state.update_data(lucky_number=user_input)
            reg_data = await state.get_data()
            await create_user_in_users(
                tg_id=message.from_user.id,
                username=reg_data['username'],
                lucky_number=reg_data['lucky_number']
            )
            await message.answer(f'{message.text}? Красивое число!\n\n'
                                 '✅ Регистрация завершена успешно.\n'
                                 'Посмотреть свой профиль можно через Кнопку "🧑 Мой профиль"',
                                 reply_markup=rk.rButtons
            )
            await state.clear()
        else:
            await message.answer("❌ Пожалуйста, введи ЦЕЛОЕ ПОЛОЖИТЕЛЬНОЕ число (например: 4, 16, 111 и т.д.):")
    except ValueError:
        await message.answer("❌ Пожалуйста, введи ЦЕЛОЕ ПОЛОЖИТЕЛЬНОЕ число (например: 4, 16, 111 и т.д.):")

"""Изменение профиля"""
@router.callback_query(F.data == 'start_change_profile')
async def changeProfile_start_step(callback: CallbackQuery, state: FSMContext):
    """Изменение профиля по инлайн кнопке 'il_ChangeProfileBtn_insideReply'."""
    await callback.answer()
    await state.set_state(ChangeProfile.new_username)
    await callback.message.answer('Введи свой новый никнейм (до 30 символов):')
@router.message(ChangeProfile.new_username)
async def changeProfile_newUsername_step(message: Message, state: FSMContext):
    user_input = message.text
    if len(user_input) > 30:
        await message.answer('❌ Никнейм слишком длинный! Максимум 30 символов. Попробуй снова:')
    elif len(user_input) == 0:
        await message.answer('❌ Никнейм не может быть пустым! Попробуй снова:')
    else:
        await state.update_data(new_username=message.text)
        await state.set_state(ChangeProfile.new_lucky_number)
        await message.answer(f'Отлично, {message.text}!\nТеперь укажи своё новое счастливое число:')
@router.message(ChangeProfile.new_lucky_number)
async def changeProfile_newLuckyNumber_step(message: Message, state: FSMContext):
    try:
        user_input = int(message.text)
        if user_input > 0:
            await state.update_data(new_lucky_number=user_input)
            profile_data = await state.get_data()
            updated_user = await update_user_in_users(
                tg_id=message.from_user.id,
                new_username=profile_data['new_username'],
                new_lucky_number=profile_data['new_lucky_number']
            )
            if updated_user:
                await message.answer(
                    f'{message.text}? Красивое число, ещё лучше предыдущего!\n\n'
                    '✅ Профиль успешно изменён.\n'
                    'Посмотреть свой новый профиль можно через Кнопку "🧑 Мой профиль"',
                    reply_markup=rk.rButtons
                )
            else:
                await message.answer(
                    '❌ Произошла ошибка при обновлении профиля.\n'
                    'Возможно, ты не зарегистрирован.',
                    reply_markup=rk.rButtons
                )
            await state.clear()
        else:
            await message.answer("❌ Пожалуйста, введи ЦЕЛОЕ ПОЛОЖИТЕЛЬНОЕ число (например: 4, 16, 111 и т.д.):")
    except ValueError:
        await message.answer("❌ Пожалуйста, введи ЦЕЛОЕ ПОЛОЖИТЕЛЬНОЕ число (например: 4, 16, 111 и т.д.):")





# @router.callback_query(F.data == 'start_change_profile')
# async def changeProfile(callback: CallbackQuery):
#     await callback.answer('Вы нажали "Изменить профиль"')  # callback.answer() убирает "мигание" кнопки после нажатия
#     await callback.message.answer('В будущем здесь можно будет поменять свой профиль.')

            ###   Состояния   ###
# @router.message(Command('reg'))
# async def reg_user_firstStep(message: Message, state: FSMContext):
#     await state.set_state(Registration.name)
#     await message.answer('Введите своё имя:')
# 
# @router.message(Registration.name)
# async def reg_user_secondStep(message: Message, state: FSMContext):
#     await state.update_data(name = message.text)
#     await state.set_state(Registration.lucky_number)
#     await message.answer('Введите своё счастливое число:')
#     
# @router.message(Registration.lucky_number)
# async def reg_user_thirdStep(message: Message, state: FSMContext):
#     await state.update_data(lucky_number = message.text)
#     reg_data = await state.get_data()
#     await message.answer(f'Регистрация завершена! Ваши данные:\nИмя: {reg_data['name']}\nСчастливое число: {reg_data['lucky_number']}')
#     await state.clear()