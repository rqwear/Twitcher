import asyncio
import logging

from data.twitchapp import CheckUser, name_of_stream
from keyboards.inline.choice_buttuns import db_callback
from loader import dp, db, bot
from aiogram import types
from filters import IsGroup, IsPrivate, AdminFilter
from aiogram.dispatcher.filters.builtin import Command


@dp.callback_query_handler(db_callback.filter(command="activate2"))
async def twitch(full_name, telegram_id):
    logging.info(f'{full_name} has activate bot sending twitch info')
    user = await db.select_user(full_name=full_name, telegram_id=telegram_id)
    a = 0
    if user[8] == 1:
        user = await db.select_user(full_name=full_name, telegram_id=telegram_id)
        activation = user[8]
        while activation == 1:
            if user[6] == None:
                await asyncio.sleep(0.1)
                await bot.send_message(chat_id=user[2], text='Вы не указали ник на твиче или указали не верно')
            else:
                if await CheckUser(user[6]) == True:
                    stream_name = await name_of_stream(user[6])
                    await bot.send_message(chat_id=int(user[5]),
                                           text=f'{stream_name}\n https://www.twitch.tv/{user[6]}')
                    await asyncio.sleep(600)
                    while await CheckUser(user[6]) == True:
                        user = await db.select_user(full_name=full_name, telegram_id=telegram_id)
                        activation = user[8]
                        if activation == 1:
                            await asyncio.sleep(600)
                        else:
                            break
                elif await CheckUser(user[6]) != True:
                    while await CheckUser(user[6]) != True:
                        user = await db.select_user(full_name=full_name, telegram_id=telegram_id)
                        activation = user[8]
                        if activation == 1:
                            await asyncio.sleep(100)
                        else:
                            break
        await asyncio.sleep(0.1)
    else:
        await bot.send_message(chat_id=user[2], text="Если вы видите это сообщение вы уже активировали бота у себя в чате либо"
                                                     "ввели данные некоректно")


@dp.message_handler(AdminFilter(), IsGroup(), Command("thisgroup"))
async def hi(message: types.Message):
    id = message.message_id
    id2 = message.chat.id
    group_name = message.chat.id
    await db.update_group_name(group_name=group_name, telegram_id=message.from_user.id)
    await db.update_is_group(is_group=1, telegram_id=message.from_user.id)
    await bot.delete_message(id2, id)


