"""Клавиатуры для админ панели."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



il_adminPanel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Отправить оповещение (всем)', callback_data='admin_panel_main')]
])