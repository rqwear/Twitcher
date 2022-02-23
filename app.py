import asyncio
import logging
import middlewares, filters, handlers  # noqa

from aiogram import executor, Dispatcher
from loader import dp, db
from restartDBactivfunction import restart_notification, table_users
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher: Dispatcher):
    # Уведомляет про запуск
    logging.info("Создаем подключение к базе данных")
    try:
        logging.info("Создаем таблицу пользователей")
        await db.create_table_users()
        logging.info("Готово.")
    except Exception as e:
        logging.info(f"{e}")

    await table_users()
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


async def on_shutdown(_: Dispatcher):
    await db.close()


if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    tasks = ioloop.create_task(restart_notification())
    executor.start_polling(dp, loop=ioloop, on_startup=on_startup, on_shutdown=on_shutdown)