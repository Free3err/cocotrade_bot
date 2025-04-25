from aiogram import Dispatcher, types


class Others:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.message.register(Others.fallback)

    @staticmethod
    async def fallback(message: types.Message):
        await message.answer("🙉 Неизвестная команда. Используй /start, чтобы начать игру.")
