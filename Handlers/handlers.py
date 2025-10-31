from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Keyboards import replyKeyboards as rk
from Keyboards import inlineKeyboards as ik

from States.states import Registration, ChangeProfile

from Database.crud import create_user_in_users, update_user_in_users, get_user_by_tg_id

from Utils.registation import get_profile_send_reply



router = Router()
    
            ###   Командные хендлеры   ###
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я живее всех живых!', reply_markup=rk.rButtons)

@router.message(Command('dice'))
async def roll_dice(message: Message):
    if get_user_by_tg_id(message.from_user.id) is None:
        await message.answer('Cначала нужно зарегистрироваться! Нажми кнопку "🧑 Мой профиль" и следуй инструкциям.')
    else:
        await message.answer_dice()

# @router.message(Command('getID'))
# async def get_id(message: Message):
#     await message.reply(f'Your ID: {message.from_user.id}\nYour name: {message.from_user.first_name}') # reply для ОТВЕТА на сообщение (как функция тг)

@router.message(Command('meme'))
async def get_meme(message: Message):
    if get_user_by_tg_id(message.from_user.id) is None:
        await message.answer('Cначала нужно зарегистрироваться! Нажми кнопку "🧑 Мой профиль" и следуй инструкциям.')
    else:
        await message.answer_photo(photo='AgACAgIAAxkBAAIDvWkCUVhOLsJ8gLOVnwGDmIsuhtarAAKY-TEb_HcRSJe2xTakO1MIAQADAgADeAADNgQ',
                                   caption='Всего ли тест картинки, не обращай внимания...',) # reply_markup=ik.iButtons

@router.message(Command('register'))
async def cmd_register(message: Message):
    await get_profile_send_reply(message)

            ###   Кнопочные хендлеры на реплай кнопки   ###
@router.message(F.text == '🧑 Мой профиль')
async def profile_button(message: Message):
    await get_profile_send_reply(message)
        
@router.message(F.text == '🎲 Бросить дайс')
async def roll_dice_button(message: Message):
    if get_user_by_tg_id(message.from_user.id) is None:
        await message.answer('Cначала нужно зарегистрироваться! Нажми кнопку "🧑 Мой профиль" и следуй инструкциям.')
    else:
        await message.answer_dice()

# @router.message(F.text == 'Найти фото (в разработке)')
# async def say_hello(message: Message):
#     await message.answer('Сказал же, что в разработке! Потом появится...')
        
            ###   Смешанные хендлеры (CMD+РеплайКнопки)   ###     
@router.message(Command('help'))
@router.message(F.text == '🔍 Помощь')
async def get_help(message: Message):
    await message.answer(
    '/help чтобы увидеть все доступные команды.\n'
    '/library чтобы войти в библиотеку бота.\n'
    '/meme просто мем.\n'
    '/dice чтобы бросить дайс.\n'
#    '/getID получить свой tg_id\n'
    '/register чтобы создать/изменить или посмотреть профиль.\n\n'
)

            ###   Коллбэки   ###
"""Регистрация."""
"""Регистрация по инлайн кнопке 'il_RegistrationProfileBtn_insideReply'."""
@router.callback_query(F.data == 'start_registration')
async def reg_start_step(callback: CallbackQuery, state: FSMContext):
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
    elif not user_input.replace('_', '').isalnum():
        await message.answer('❌ Никнейм может содержать только буквы, цифры и "_". Попробуй снова:')
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
                tg_username=message.from_user.username,
                tg_first_name=message.from_user.first_name,
                tg_last_name=message.from_user.last_name,
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

"""Изменение профиля."""
"""Изменение профиля по инлайн кнопке 'il_ChangeProfileBtn_insideReply'."""
@router.callback_query(F.data == 'start_change_profile')
async def changeProfile_start_step(callback: CallbackQuery, state: FSMContext):
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

            ###   Прочие хендлеры   ###
@router.message(F.photo)                            
async def get_photo(message: Message):
    if get_user_by_tg_id(message.from_user.id) is None:
        await message.answer('Cначала нужно зарегистрироваться! Нажми кнопку "🧑 Мой профиль" и следуй инструкциям.')
    else:
        await message.answer(f'Your Photo_ID: {message.photo[-1].file_id}')

@router.message(F.text == 'Hello') # ECHO test
async def say_hello(message: Message):
    await message.answer('Hello mate!')

@router.message() # хендлер для случайных сообщений. Всегда должен быть ниже всех остальных хендлеров!
async def uncnown_message(message: Message):
    await message.answer(
        '🤔 Хм-м... Я что-то не совсем тебя понял.\n'
        'Если тебе что-то нужно, лучше обратись за помощью командой /help или через меню бота!'
    )