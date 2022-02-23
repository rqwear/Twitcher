from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

db_callback = CallbackData("addtobase", "command")
db_manual =CallbackData("manual", "command", "Name", "id")



def add_to_db():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Добавить(изменить) ник стримера на Twitch",
            callback_data=db_callback.new(command="twitchname")

        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Добавить(изменить) в группу",
            callback_data=db_callback.new(command="groupname")

        )
    )
    markup.row(
        InlineKeyboardMarkup(
            text="Проверить данные и активировать бота группе",
            callback_data=db_callback.new(command="check_data")
        )
    )
    return markup


def check_group():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Продолжить",
            callback_data=db_callback.new(command="cheking_group")

        )
    )
    return markup

def activate():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Активировать",
            callback_data=db_callback.new(command="activate")

        )
    )
    return markup

def manual_keyboard(Name, id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Активировать",
            callback_data=db_manual.new(command="man", Name=Name, id=id)

        )
    )
    return markup

def exit_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Отмена",
            callback_data=db_callback.new(command="exit")

        )
    )
    markup.row(
        InlineKeyboardButton(
            text='Ввести еще раз',
            callback_data=db_callback.new(command="enter_nick")
        )
    )
    return markup