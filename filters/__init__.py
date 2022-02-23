from aiogram import Dispatcher
from .in_group import IsGroup
from .in_private import IsPrivate
from .Admins import AdminFilter
from  .bot_owner import BotOwner


# from .is_admin import AdminFilter


def setup(dp: Dispatcher):
    # dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(BotOwner)

