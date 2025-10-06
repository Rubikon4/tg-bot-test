from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Keybords import replyKeyboards as rk
from Keybords import inlineKeyboards as ik
from States.states import Registation as reg
from aiogram.fsm.context import FSMContext

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
                               caption='AHAHAHAHAHAHAHH AHAHHAH AHHA haha.....', reply_markup=ik.iButtons
    )

            ###   Текстовые хендлеры   ###
@router.message(F.text == 'Hello')
async def say_hello(message: Message):
    await message.answer('Hello mate!')

@router.message(F.text == 'Мой профиль')
async def get_profile(message: Message):
    await message.answer(
        'Ваш профиль:\nСкоро здесь будет информация о вас...',
        reply_markup=ik.inlineProfile
    )    

@router.message(F.text == 'Бросить дайс')
async def roll_dice(message: Message):
    await message.answer_dice()
        
            ###   Смешанные хендлеры (Command+Text)   ###     
@router.message(Command('help'))
@router.message(F.text == 'Помощь')
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

            ###   Колбэки   ###
@router.callback_query(F.data == 'change_profile')
async def changeProfile(callback: CallbackQuery):
    await callback.answer('Вы нажали "Изменить профиль"')  # callback.answer() убирает "мигание" кнопки после нажатия
    await callback.message.answer('Здесь можно будет поменять свой профиль')

            ###   Состояния   ###
@router.message(Command('reg'))
async def reg_user_firstStep(message: Message, state: FSMContext):
    await state.set_state(reg.name)
    await message.answer('Введите своё имя:')

@router.message(reg.name)
async def reg_user_secondStep(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(reg.lucky_number)
    await message.answer('Введите своё счастливое число:')
    
@router.message(reg.lucky_number)
async def reg_user_thirdStep(message: Message, state: FSMContext):
    await state.update_data(lucky_number = message.text)
    reg_data = await state.get_data()
    await message.answer(f'Регистрация завершена! Ваши данные:\nИмя: {reg_data['name']}\nСчастливое число: {reg_data['lucky_number']}')
    await state.clear() 