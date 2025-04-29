from aiogram import Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Store:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(Store.common_store, F.data == "store")
        dispatcher.callback_query.register(Store.donut_store, F.data == "donut_store")

        # dispatcher.callback_query.register(Store.coconut_seems, F.data == "coconut_seems")
        # dispatcher.callback_query.register(Store.fertilizers, F.data == "fertilizers")
        # dispatcher.callback_query.register(Store.donut, F.data == "donut")
        # dispatcher.callback_query.register(Store.experimental_coconut_seems, F.data == "experimental_coconut_seems")

    @staticmethod
    async def common_store(callback_query: types.CallbackQuery):
        buttons = [[InlineKeyboardButton(text="🥥 Семена кокосов", callback_data="coconuts_seems")],
                   [InlineKeyboardButton(text="🌱 Удобрения", callback_data="fertilizers")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stores_menu")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🏪 <b>Добро пожаловать в обычный магазин!</b>\n"
                                               "\n"
                                               "Наш ассортимент представлен ниже:", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def donut_store(callback_query: types.CallbackQuery):
        buttons = [[InlineKeyboardButton(text="🕊️ Пожертвование", callback_data="donut")],
                   [InlineKeyboardButton(text="🥥 Экспериментальные кокосы",
                                         callback_data="experimental_coconuts_seems")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stores_menu")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text(f"🏬 <b>Добро пожаловать в donut магазин!</b>\n"
                                               f"\n"
                                               f"Здесь можно попытать себя в удаче или пожертововать разработчику "
                                               f"на пропитание!", parse_mode="HTML", reply_markup=markup
                                               )

    @staticmethod
    async def coconuts_seems(callback_query: types.CallbackQuery):
        pass

    @staticmethod
    async def fertilizers(callback_query: types.CallbackQuery):
        pass

    @staticmethod
    async def selected_store_item(callback_query: types.CallbackQuery):
        pass
