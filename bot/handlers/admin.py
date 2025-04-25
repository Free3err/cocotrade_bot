from aiogram import Dispatcher
from aiogram.filters import Command


class Admin:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.message.register(Admin.admin, Command("/admin"))

    async def admin(self):
        pass

    async def manage_user(self):
        pass

    async def manage_stores_items(self):
        pass
