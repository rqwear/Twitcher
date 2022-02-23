from aiogram import types
from aiogram.dispatcher import FSMContext
from twitchAPI import Twitch
from handlers.groups.main import twitch as act
from keyboards.inline.choice_buttuns import db_callback, add_to_db, check_group, activate, exit_keyboard
from loader import dp, db, bot
from data.config import TWITCH_ID, TWITCH_SECRET


client_id = TWITCH_ID
client_secret = TWITCH_SECRET

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

@dp.callback_query_handler(db_callback.filter(command="twitchname"))
async def enter_twitch_name_from_button(callback: types.CallbackQuery, state: FSMContext):
    await db.update_activation(activation=0, telegram_id=callback.from_user.id)
    await callback.message.answer('Напиши ник стримера для получение оповещений в группе')
    await state.set_state(state="twitch_name_from_button")


@dp.message_handler(state="twitch_name_from_button")
async def add_twitchname_to_db(message: types.Message, state: FSMContext):
    twitch_name = message.text
    try:
        user_info = twitch.get_users(logins=[twitch_name])
        user_description = user_info['data'][0]['description']
        await db.update_twitch_name(twitch_name=twitch_name, telegram_id=message.from_user.id)
        user = await db.select_user(telegram_id=message.from_user.id)
        await message.answer(f"twitch.tv/{user[6]} \n"
                             f"{user_description}")
        await message.answer(f"Данные обновлены. Ник на твиче: {user[6]}", reply_markup=add_to_db())
        await state.finish()
    except:
        await message.answer(f"Такого стримера не существует", reply_markup=exit_keyboard())
        await state.finish()

@dp.callback_query_handler(db_callback.filter(command="exit"))
async def exit(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Выбирите действие", reply_markup=add_to_db())
    await state.finish()

@dp.callback_query_handler(db_callback.filter(command="enter_nick"))
async def exit(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Напиши ник стримера:')
    await state.set_state(state="twitch_name_from_button")



@dp.callback_query_handler(db_callback.filter(command="groupname"))
async def enter_twitch_name_from_button(callback: types.CallbackQuery):
    await callback.message.answer(text='Добавь бота в группу, дай ему админку и введи команду /thisgroup в группе после чего нажми кнопку продолжить(на данный момент доступна лишь одна группа)',
                                  reply_markup=check_group())



@dp.callback_query_handler(db_callback.filter(command="cheking_group"))
async def cheking_group(callback: types.Message):
    try:
        user = await db.select_user(full_name=callback.from_user.full_name, telegram_id=callback.from_user.id)
        group_name = user[5]
        if group_name is not None:
            await callback.message.answer(text=f'Группа добавлена')
            await callback.message.answer(text='Активируйте бота', reply_markup=add_to_db())
            await db.update_is_group(is_group=1, telegram_id=callback.from_user.id)
            await db.update_activation(activation=0, telegram_id=callback.from_user.id)
        else:
            await callback.message.answer(text=f'Бот не добавлен, попробуйте еще раз и нажмите кнопку продолжить',
                                          reply_markup=check_group())
    except Exception as e:
        print(e)


@dp.callback_query_handler(db_callback.filter(command="check_data"))
async def check_data(callback: types.CallbackQuery):
    try:
        user = await db.select_user(full_name=callback.from_user.full_name, telegram_id=callback.from_user.id)
        group_name = user[5]
        twitch_name = user[6]
        activation = user[8]
        if group_name and twitch_name is not None and activation == 0:
            await db.update_is_group(is_group=1, telegram_id=callback.from_user.id)
            await callback.message.answer(text='Данные верны', reply_markup=activate())
        elif group_name and twitch_name is not None and activation == 1:
            await callback.message.answer(text=f'Бот уже активирован')
        else:
            await callback.message.answer(text=f'Данные не верны заполните ник стримера {twitch_name}, id группы {group_name}',
                                          reply_markup=add_to_db())
    except Exception as e:
        print(e, "check data")



@dp.callback_query_handler(db_callback.filter(command="activate"))
async def check_data(callback: types.CallbackQuery):
    try:
        await db.update_activation(activation=1, telegram_id=callback.from_user.id)
        full_name = callback.from_user.full_name
        telegram_id = callback.from_user.id
        await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
        await callback.message.answer(text='Бот успешно активирован')
        await act(full_name=full_name, telegram_id=telegram_id)
    except Exception as e:
        print(e, 'activate')

