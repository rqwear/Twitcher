from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import BOT_OWNER


class BotOwner(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = message.from_user.id
        if member == BOT_OWNER:
            return True
        else:
            return False