import asyncio
import logging

from data.twitchapp import CheckUser
from handlers.groups.main import twitch
from loader import db, bot

class AsyncIter:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item


async def table_users():
    global users_for_restart
    users_for_restart = await db.select_all_users()


async def restart_notification():
    await asyncio.sleep(10)
    users = users_for_restart
    logging.info("Auto sending activated")
    await asyncio.sleep(2)
    try:
        await asyncio.gather(*(twitch(user[1], user[2]) for user in users if user[8] == 1), asyncio.sleep(0.1))
    except Exception as err:
        logging.exception(err)