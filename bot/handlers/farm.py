from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.handlers import MainMenu
from bot.services import UserRequests, TechnologyRequests


class FarmStates(StatesGroup):
    in_tech_store = State()


class Farm:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(Farm.collect, F.data == 'collect')
        dispatcher.callback_query.register(Farm.my_crops, F.data == 'my_crops')
        dispatcher.callback_query.register(Farm.technologies_store, F.data == 'technologies_store')

    @staticmethod
    async def collect(callback_query: CallbackQuery):
        user = UserRequests.get(callback_query.from_user.id)
        new_coconut_balance = user['coconut_balance'] + user['farm']['uncollected']
        if UserRequests.patch(callback_query.from_user.id,
                              {'coconut_balance': new_coconut_balance, 'farm': {'uncollected': 0}}):
            await MainMenu.farm(callback_query)

    @staticmethod
    async def my_crops(callback_query: CallbackQuery):
        user = UserRequests.get(callback_query.from_user.id)

        buttons = [[InlineKeyboardButton(text="🔙 Назад", callback_data='farm')]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🏝️ <b>Ваши посевы:</b>\n"
                                               "\n"
                                               f"🥥 <b>Кокос:</b> {user['farm']['coconut']['name']}\n"
                                               f"🌱 <b>Посажено:</b> {user['farm']['coconuts_count']} штук\n"
                                               f"🕑 <b>Плодоносимость:</b> {user['farm']['coconut']['amount_per_hour']}/час\n"
                                               f"📃 <b>Описание:</b> {user['farm']['coconut']['description']}\n"
                                               "\n"
                                               f"🚀 <b>Технология выращивания:</b> {user['farm']['technology']['name']}\n"
                                               f"💹 <b>Множитель:</b> {user['farm']['technology']['multiplier']}x\n"
                                               f"📃 <b>Описание:</b> {user['farm']['technology']['description']}",
                                               parse_mode='HTML', reply_markup=markup)

    @staticmethod
    async def technologies_store(callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(FarmStates.in_tech_store)

        technologies = TechnologyRequests.get_all()
        await state.update_data(technologies=technologies)

        buttons = [[InlineKeyboardButton(text=tech['name'], callback_data=f"chosen_tech_view.{tech['id']}")] for tech in technologies]
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='farm')])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🚀 <b>Технологии, доступные к приобритению и установке:</b>",
                                               parse_mode="HTML", reply_markup=markup)
