import logging
from aiogram.dispatcher.filters import Command
from handlers.groups.main import twitch as act
from filters import IsPrivate, BotOwner
from keyboards.inline.choice_buttuns import db_manual
from loader import dp, db, bot
from aiogram import types
from keyboards.inline.choice_buttuns import manual_keyboard


@dp.message_handler(IsPrivate(), BotOwner(), Command("manualon"))
async def bot_start(message: types.Message):
    users = await db.select_all_users()
    count = await db.count_users()
    active_count = 0
    for i in users:
        if i[8] == 1:
            active_count += 1
            Name = i[1]
            id = i[2]
            await message.answer(text=f'Активировать для пользователя {Name}', reply_markup=manual_keyboard(Name, id))
            logging.info(f'manual activation')
    await message.answer(text=f'Юзеров всего {count} , активных {active_count}')

@dp.callback_query_handler(db_manual.filter(command="man"))
async def manual_activation(callback: types.CallbackQuery, callback_data: dict):
    try:
        Name = callback_data.get("Name")
        id = int(callback_data.get("id"))
        logging.info(f'activativate for {Name}')
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
        await callback.answer(text=f'Бот для {Name} успешно активирован')
        await act(Name, id)
    except Exception as e:
        print(e)