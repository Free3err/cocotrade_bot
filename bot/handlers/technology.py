from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services import UserRequests


class Technology:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(Technology.chosen_tech_view, F.data.contains('chosen_tech_view'))
        dispatcher.callback_query.register(Technology.buy_chosen_tech, F.data == 'buy_technology')

    @staticmethod
    async def chosen_tech_view(callback_query: CallbackQuery, state: FSMContext):
        buttons = [[InlineKeyboardButton(text="💰 Приобрести", callback_data="buy_technology")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="technologies_store")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        tech_data = await get_chosen_tech(callback_query, state)
        await state.update_data(chosen_tech_data=tech_data)
        await callback_query.message.edit_text(f"🚀 <b>{tech_data['name']}</b>\n"
                                               f"💹 <b>Множитель:</b> {tech_data['multiplier']}x\n"
                                               f"📃 <b>Описание:</b> {tech_data['description']}\n"
                                               "\n"
                                               f"💵 <b>Стоимость:</b> {tech_data['price']} кокосов", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def buy_chosen_tech(callback_query: CallbackQuery, state: FSMContext):
        state_data = await state.get_data()
        chosen_tech_data = state_data['chosen_tech_data']

        user = UserRequests.get(callback_query.from_user.id)

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 В магазин", callback_data="technologies_store")]])
        if user['farm']['technology']['id'] == chosen_tech_data['id']:
            await callback_query.message.edit_text(
                "❌ <b>Вы не можете приобрести технологию, которую используете в данный момент!</b>", parse_mode="HTML",
                reply_markup=markup)
        elif (user['coconut_balance'] - chosen_tech_data['price'] >= 0 and
              UserRequests.patch(callback_query.from_user.id,
                                 {
                                     'coconut_balance': user[
                                                            'coconut_balance'] -
                                                        chosen_tech_data[
                                                            'price'],
                                     'farm': {
                                         'technology': {
                                             'id':
                                                 chosen_tech_data[
                                                     'id']
                                         }
                                     }
                                 })):
            await callback_query.message.edit_text(
                f"✅ <b>Вы успешно приобрели технологию выращивания: {chosen_tech_data['name']}!</b>", parse_mode="HTML",
                reply_markup=markup)
        else:
            await callback_query.message.edit_text("❌ <b>Недостаточно кокосов для приобретения данной технологии!</b>",
                                                   parse_mode="HTML", reply_markup=markup)
        await state.clear()


async def get_chosen_tech(callback_data: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tech_id = int(callback_data.data.split(".")[1])
    chosen_tech = [tech for tech in state_data['technologies'] if tech['id'] == tech_id][0]

    return chosen_tech
