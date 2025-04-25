from aiogram import types, Dispatcher, F
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command


class MainMenu:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.message.register(MainMenu.start, Command("start"))
        dispatcher.message.register(MainMenu.farm, F.text.contains("🥥 Ферма"))
        dispatcher.message.register(MainMenu.store, F.text.contains("🛍️ Магазин"))
        dispatcher.message.register(MainMenu.travels, F.text.contains("✈️ Путешествия"))
        dispatcher.message.register(MainMenu.statistic, F.text.contains("📉 Статистика"))
        dispatcher.message.register(MainMenu.about, F.text.contains("🏝️ О проекте"))

        dispatcher.callback_query.register(MainMenu.store, F.data == "back_to_stores_menu")

    @staticmethod
    async def start(message: types.Message) -> None:
        buttons = [[KeyboardButton(text="🥥 Ферма")],
                   [KeyboardButton(text="🛍️ Магазин"), KeyboardButton(text="✈️ Путешествия")],
                   [KeyboardButton(text="📉 Статистика")],
                   [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="🏝️ О проекте")]]
        markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await message.answer(f"🌴 <b>Привет, {message.from_user.first_name}!</b>\n"
                             f"\n"
                             f"🥥 Добро пожаловать в <b>CocoTrade</b> - экономическую игру, построенную на кокосах!\n"
                             f"🚀 Начинай с маленькой фермы и стань монополистом в сфере кокосов!\n"
                             f"\n"
                             f"🧑‍💻 <b>Разработчик - @free3err</b>", parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def farm(query: types.Message | types.CallbackQuery) -> None:
        buttons = [[InlineKeyboardButton(text="🥥 Собрать урожай", callback_data='collect')],
                   [InlineKeyboardButton(text="🏝️ Мои посевы", callback_data='my_crops'),
                    InlineKeyboardButton(text="🚀 Улучшения", callback_data='upgrades')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer("🥥 Добро пожаловать на ферму!", parse_mode="HTML", reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text("🥥 Добро пожаловать на ферму!", parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def store(query: types.Message | types.CallbackQuery) -> None:
        buttons = [[InlineKeyboardButton(text="🏪 Обычный магазин", callback_data='store')],
                   [InlineKeyboardButton(text="🏬 VIP магазин", callback_data='donut_store')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer(".", parse_mode="HTML", reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text(".", parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def travels(query: types.Message | types.CallbackQuery) -> None:
        cur_pos = None

        buttons = [[InlineKeyboardButton(text="🧭 Локации", callback_data='locations')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer(f"🧳 Сейчас Вы находить в {cur_pos}!", parse_mode="HTML", reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text(" Сейчас Вы находить в {cur_pos}!", parse_mode="HTML",
                                              reply_markup=markup)

    @staticmethod
    async def statistic(message: types.Message) -> None:
        statistics = {}
        await message.answer(f"📉 Статистика проекта CocoTrade\n"
                             f"\n"
                             f"👥 Кол-во ферм: {statistics.get('count_farms', None)}\n"
                             f"🥥 Всего кокосов: {statistics.get('count_coconut', None)}\n"
                             f"💸 Донатов на сумму: {statistics.get('count_donuts', None)}\n", parse_mode="HTML")

    @staticmethod
    async def about(message: types.Message) -> None:
        buttons = [[InlineKeyboardButton(text="👨‍⚖️ Правила", url="https://telegra.ph/Pravila-CocoTrade-04-25")],
                   [InlineKeyboardButton(text="📜 Условия Использования",
                                         url="https://telegra.ph/Usloviya-ispolzovaniya-CocoTrade-04-25"),
                    InlineKeyboardButton(text="🪪 Политика конфиденциальности",
                                         url="https://telegra.ph/Politika-Konfidencialnosti-CocoTrade-04-25")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(f"🥥 <b>CocoTrade: экономика на кокосах</b>\n"
                             f"\n"
                             f"Это игровой экономический проект, "
                             f"направленный на развитие понятия работы рынка и других механик "
                             f"экономики обычном людям.\n"
                             f"\n"
                             f"❓ <b>Идея игры проста - Вы начинающий магнат, владеющий небольшой фермой кокосов.</b>\n"
                             f"🚀 Разваивайте свой бизнес, покупая новые сорта мохнатых орехов "
                             f"или меняя технологию их выращивания, а после - попробуйте вывести новые семена или купите "
                             f"их на торговой бирже у других игроков.\n"
                             f"\n"
                             f"🧑‍💻 <b>Разработчик - @free3err, личный проект для Яндекс.Лицея</b>",
                             parse_mode="HTML", reply_markup=markup)
