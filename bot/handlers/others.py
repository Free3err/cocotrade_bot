from aiogram import Dispatcher, types, Router
from aiogram.fsm.state import default_state

fallback_router = Router()


class Others:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.include_router(fallback_router)

    @staticmethod
    @fallback_router.message(default_state)
    async def fallback(message: types.Message):
        await message.answer("🙉 Неизвестная команда. Используй /start, чтобы начать игру.")
