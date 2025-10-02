from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from Keybords import replyKeyboards as rk
from Keybords import inlineKeyboards as ik

router = Router()

@router.message(CommandStart())
async def   cmd_start(message: Message):
    await message.answer('Hello! bot is running... Type /help for commands list.', reply_markup=rk.rButtons)
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('/help to get to get commands list\n/meme to get funny meme lol\n/dice to throw dice\n/getID to get your personal ID')
@router.message(Command('dice'))
async def get_help(message: Message):
    await message.answer_dice()
@router.message(Command('getID'))
async def get_help(message: Message):
    await message.reply(f'Your ID: {message.from_user.id}\nYour name: {message.from_user.first_name}') # reply для ОТВЕТА на сообщение (как функция тг)
@router.message(Command('meme'))
async def get_help(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMxaN0uaIVb7R4yLWBLZORJ0U3IUVEAAtD7MRueBelKtCJgPakJ0xIBAAMCAAN5AAM2BA',
                               caption='AHAHAHAHAHAHAHH AHAHHAH AHHA haha.....', reply_markup=ik.iButtons)
@router.message(F.text=='Hello')
async def say_hello(message: Message):
    await message.answer('Hello mate!')
@router.message(F.photo)                            
async def get_photo(message: Message):
    await message.answer(f'Your Photo_ID: {message.photo[-1].file_id}')