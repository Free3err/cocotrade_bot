import asyncio
from aiogram import Bot, Dispatcher

from bot.handlers import *
from config import EnvConfig

dispatcher = Dispatcher()


class CocoTradeBot:
    def __init__(self) -> None:
        self.token = EnvConfig.TOKEN
        self.bot = Bot(token=self.token)

    async def start_bot(self) -> None:
        await self.init_handlers()
        await self.init_dispatcher()

    async def init_dispatcher(self) -> None:
        await dispatcher.start_polling(self.bot)

    @staticmethod
    async def init_handlers() -> None:
        AdminManagingAccount.register_all(dispatcher)
        ManagingAccount.register_all(dispatcher)
        MainMenu.register_all(dispatcher)
        Farm.register_all(dispatcher)
        Admin.register_all(dispatcher)
        Store.register_all(dispatcher)
        Others.register_all(dispatcher)


if __name__ == '__main__':
    bot = CocoTradeBot()
    asyncio.run(bot.start_bot())
