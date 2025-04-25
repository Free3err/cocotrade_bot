from aiogram import types, Dispatcher, F
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.filters import Command


class MainMenu:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.message.register(MainMenu.start, Command("start"))
        dispatcher.message.register(MainMenu.farm, F.text.contains("🥥 Ферма"))
        dispatcher.message.register(MainMenu.store, F.text.contains("🛍️ Магазин"))

        dispatcher.callback_query.register(MainMenu.store, F.data == "back_to_stores_menu")

    @staticmethod
    async def start(message: types.Message) -> None:
        buttons = [[KeyboardButton(text="🥥 Ферма")],
                   [KeyboardButton(text="🛍️ Магазин"), KeyboardButton(text="✈️ Путешествия")],
                   [KeyboardButton(text="📉 Статистика")],
                   [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="🏝️ О проекте")]]
        markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await message.answer(f"🌴 <b>Привет, {message.from_user.first_name}!</b>\n"
                             f"\n"
                             f"🥥 Добро пожаловать в <b>CocoTrade</b> - экономическую игру, построенную на кокосах!\n"
                             f"🚀 Начинай с маленькой фермы и стань монополистом в сфере кокосов!\n"
                             f"\n"
                             f"🧑‍💻 <b>Разработчик - @free3err</b>", parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def farm(message: types.Message) -> None:
        buttons = [[InlineKeyboardButton(text="🥥 Собрать урожай", callback_data='collect')],
                   [InlineKeyboardButton(text="🏝️ Мои посевы", callback_data='my_crops'),
                    InlineKeyboardButton(text="🚀 Улучшения", callback_data='upgrades')]]
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer("🥥 Добро пожаловать на ферму!", parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def store(query: types.Message | types.CallbackQuery) -> None:
        buttons = [[InlineKeyboardButton(text="🏪 Обычный магазин", callback_data='store')],
                   [InlineKeyboardButton(text="🏬 VIP магазин", callback_data='donut_store')]]
        markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer(".", parse_mode="HTML", reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text(".", parse_mode="HTML", reply_markup=markup)
