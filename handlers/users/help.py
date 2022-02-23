from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler()
async def bot_help(message: types.Message):
    text = [
        'Введи ник любимого стримера на Twitch',
        'И узнай онлайн ли он'
    ]
    await message.answer('\n'.join(text))
