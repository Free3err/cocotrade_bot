from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

from bot.services import UserRequests


class MainMenu:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.message.register(MainMenu.start, Command("start"))
        dispatcher.message.register(MainMenu.farm, F.text.contains("🥥 Ферма"))
        dispatcher.message.register(MainMenu.store, F.text.contains("🛍️ Магазин"))
        dispatcher.message.register(MainMenu.travels, F.text.contains("✈️ Путешествия"))
        dispatcher.message.register(MainMenu.statistic, F.text.contains("📉 Статистика"))
        dispatcher.message.register(MainMenu.settings, F.text.contains("⚙️ Настройки"))
        dispatcher.message.register(MainMenu.about, F.text.contains("🏝️ О проекте"))

        dispatcher.callback_query.register(MainMenu.store, F.data == "back_to_stores_menu")
        dispatcher.callback_query.register(MainMenu.farm, F.data == "farm")

    @staticmethod
    async def start(message: types.Message) -> None:
        user = UserRequests.get(message.from_user.id)
        if not user:
            UserRequests.register(message.from_user.id)

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
    async def farm(query: types.Message | types.CallbackQuery, state: FSMContext | None = None) -> None:
        if state:
            await state.clear()

        buttons = [[InlineKeyboardButton(text="🥥 Собрать урожай", callback_data='collect')],
                   [InlineKeyboardButton(text="🏝️ Мои посевы", callback_data='my_crops'),
                    InlineKeyboardButton(text="🚀 Технологии", callback_data='technologies_store')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                user_data = UserRequests.get(query.from_user.id)
                growing_speed = round(
                    user_data['farm']['coconuts_count'] * user_data['farm']['coconut']['amount_per_hour'] * \
                    user_data['farm']['technology']['multiplier'])

                await query.answer("🥥 <b>Добро пожаловать на ферму!</b>\n"
                                   f"\n"
                                   f"🌱 Выросло на ферме: <b> {user_data['farm']['uncollected']} кокосов</b>\n"
                                   f"🕑 Скорость созревания: <b>{growing_speed} кокосов/час</b>\n"
                                   f"\n"
                                   f"🏦 Кокосовый баланс: <b>{user_data['coconut_balance']} кокосов</b>\n"
                                   f"💵 Рублевый баланс: <b>{user_data['rub_balance']} рублей</b>",
                                   parse_mode="HTML",
                                   reply_markup=markup)
            case types.CallbackQuery:
                user_data = UserRequests.get(query.from_user.id)
                growing_speed = round(
                    user_data['farm']['coconuts_count'] * user_data['farm']['coconut']['amount_per_hour'] * \
                    user_data['farm']['technology']['multiplier'])

                await query.message.edit_text("🥥 <b>Добро пожаловать на ферму!</b>\n"
                                              f"\n"
                                              f"🌱 Выросло на ферме: <b> {user_data['farm']['uncollected']} кокосов</b>\n"
                                              f"🕑 Скорость созревания: <b>{growing_speed} кокосов/час</b>\n"
                                              f"\n"
                                              f"🏦 Кокосовый баланс: <b>{user_data['coconut_balance']} кокосов</b>\n"
                                              f"💵 Рублевый баланс: <b>{user_data['rub_balance']} рублей</b>",
                                              parse_mode="HTML",
                                              reply_markup=markup)

    @staticmethod
    async def store(query: types.Message | types.CallbackQuery) -> None:
        buttons = [[InlineKeyboardButton(text="🏪 Обычный магазин", callback_data='store')],
                   [InlineKeyboardButton(text="🏬 VIP магазин", callback_data='donut_store')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer("🛍️ <b>Выберите, пожалуйста, требуемый магазин:</b>", parse_mode="HTML",
                                   reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text("🛍️ <b>Выберите, пожалуйста, требуемый магазин:</b>", parse_mode="HTML",
                                              reply_markup=markup)

    @staticmethod
    async def travels(query: types.Message | types.CallbackQuery) -> None:

        buttons = [[InlineKeyboardButton(text="🧭 Локации", callback_data='locations')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                user_data = UserRequests.get(query.from_user.id)
                await query.answer(f"🧳 <b>Сейчас Вы находить в {user_data['location']['name']}!</b>", parse_mode="HTML",
                                   reply_markup=markup)
            case types.CallbackQuery:
                user_data = UserRequests.get(query.message.from_user.id)
                await query.message.edit_text(f"🧳 <b>Сейчас Вы находитесь в {user_data['location']['name']}!</b>",
                                              parse_mode="HTML",
                                              reply_markup=markup)

    @staticmethod
    async def statistic(message: types.Message) -> None:
        statistics = {}
        await message.answer(f"📉 <b>Статистика проекта CocoTrade</b>\n"
                             f"\n"
                             f"👥 Кол-во ферм: <b>{statistics['count_farms']}</b>\n"
                             f"🥥 Всего кокосов: <b>{statistics['count_coconut']}</b>\n"
                             f"💸 Донатов на сумму: <b>{statistics['count_donuts']} рублей</b>",
                             parse_mode="HTML")

    @staticmethod
    async def settings(query: types.Message | CallbackQuery) -> None:
        user_data = UserRequests.get(query.from_user.id)

        buttons = [[InlineKeyboardButton(text="🔇 Отписаться от рассылок",
                                         callback_data='unsubscribe_on_spam') if user_data[
            'is_subscribed_on_spam'] else InlineKeyboardButton(
            text="🔊 Подписаться на рассылки", callback_data='subscribe_on_spam')],
                   [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data='delete_account')]]
        if user_data['role']['id'] == 0:
            buttons.append([InlineKeyboardButton(text="🧑‍💻 Админ-панель", callback_data='admin_panel')])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        match type(query):
            case types.Message:
                await query.answer("⚙️ <b>Добро пожаловать в меню настроек!</b>", parse_mode="HTML",
                                   reply_markup=markup)
            case types.CallbackQuery:
                await query.message.edit_text("⚙️ <b>Добро пожаловать в меню настроек!</b>", parse_mode="HTML",
                                              reply_markup=markup)

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
