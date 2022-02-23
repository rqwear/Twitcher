import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from keyboards.inline.choice_buttuns import add_to_db
from loader import dp, db
from aiogram.dispatcher.filters.builtin import Command


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    count = await db.count_users()
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Для начала работы перейди в меню и выбери меню для добавления бота'
            ]))


@dp.message_handler(IsPrivate(), Command("addbot"))
async def add_bot(callback: types.CallbackQuery):
    await callback.answer(text='Меню активации бота. Выполни все пункты что бы активировать бота у себя в группе',
                          reply_markup=add_to_db())

