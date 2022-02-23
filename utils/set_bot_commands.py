from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("addbot", "Меню для добавления бота в группу"),
        types.BotCommand("thisgroup", "Добавить в эту группу"),
    ])