from aiogram import Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Store:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(Store.common_store, F.data == "store")
        # dispatcher.callback_query.register(Store.donut_store, callback="donut_store")

    @staticmethod
    async def common_store(callback_query: types.CallbackQuery):
        buttons = [[InlineKeyboardButton(text="🥥 Семена кокосов", callback_data="coconuts_seems")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stores_menu")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🏪 <b>Добро пожаловать в обычный магазин!</b>\n"
                                               "\n"
                                               "Наш ассортимент представлен ниже:", parse_mode="HTML",
                                               reply_markup=markup)
