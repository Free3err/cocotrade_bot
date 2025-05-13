from aiogram import Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.services import CoconutRequests, UserRequests, PaymentRequests, DonationRequests

store_router = Router()


class StoreStates(StatesGroup):
    selecting_item = State()
    input_quantity = State()


class Store:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.include_router(store_router)

        dispatcher.callback_query.register(CommonStore.common_store, F.data == "common_store")
        dispatcher.callback_query.register(DonateStore.donate_store, F.data == "donate_store")

        dispatcher.callback_query.register(CommonStore.coconuts_seems, F.data == "coconuts_seems")
        dispatcher.callback_query.register(CommonStore.chosen_coco_view, F.data.contains("chosen_coco_view"))

        dispatcher.callback_query.register(DonateStore.donate_sum_input_handler, F.data == "donate_sum_input_handler")
        dispatcher.callback_query.register(DonateStore.check_payment_status, F.data.contains("check_payment"))

        dispatcher.callback_query.register(CommonStore.input_quantity_handler, F.data == "input_quantity_handler")


class CommonStore:
    @staticmethod
    async def common_store(callback_query: types.CallbackQuery):
        buttons = [[InlineKeyboardButton(text="🥥 Семена кокосов", callback_data="coconuts_seems")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_stores_menu")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🏪 <b>Добро пожаловать в обычный магазин!</b>\n"
                                               "\n"
                                               "<b>Наш ассортимент представлен ниже:</b>", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def coconuts_seems(callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(StoreStates.selecting_item)
        coconuts = CoconutRequests.get_all()
        await state.update_data(coconuts_data=coconuts, callback_data="coconuts_seems")

        buttons = [[InlineKeyboardButton(text=coco['name'], callback_data=f"chosen_coco_view.{coco['id']}")] for coco in
                   coconuts]
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="common_store")])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text("🥥 <b>Наш ассортимент сортов кокоса представлен ниже:</b>\n"
                                               "\n"
                                               "❗ <b>Учтите, что при покупке нового вида кокоса, "
                                               "отличающегося от Вашего текущего, все предыдущие посевы \"сгорают\"!</b>",
                                               parse_mode="HTML", reply_markup=markup)

    @staticmethod
    async def chosen_coco_view(callback_query: types.CallbackQuery, state: FSMContext):
        chosen_coco = await get_chosen_item(callback_query, state)
        await state.update_data(chosen_coco=chosen_coco)

        buttons = [[InlineKeyboardButton(text="💰 Приобрести", callback_data="input_quantity_handler")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data="coconuts_seems")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text(f"🥥 <b>{chosen_coco['name']}</b>\n"
                                               f"🕐 <b>Плодоносимость:</b> {chosen_coco['amount_per_hour']} кокосов/час\n"
                                               f"🧪 <b>Экспериментальный:</b> {'Да' if chosen_coco['is_experimental'] else 'Нет'}\n"
                                               f"📃 <b>Описание:</b> {chosen_coco['description']}\n"
                                               "\n"
                                               f"💵 <b>Стоимость:</b> {chosen_coco['price']} кокосов", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def input_quantity_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(StoreStates.input_quantity)
        state_data = await state.get_data()

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад",
                                                   callback_data=f"chosen_coco_view.{state_data['chosen_coco']['id']}")]])
        await callback_query.message.edit_text("✍️ <b>Введите кол-во покупаемого продукта:</b>", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def buy_chosen_coconut(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        user = UserRequests.get(message.from_user.id)
        coco_data = state_data['chosen_coco']
        quantity = state_data['quantity']
        total_price = coco_data['price'] * quantity

        back_button = InlineKeyboardButton(text="🔙 Назад", callback_data="coconuts_seems")
        markup = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

        if user['coconut_balance'] < total_price:
            await message.answer(
                "❌ <b>Недостаточно средств для приобретения указанного количества кокосов!</b>",
                parse_mode="HTML",
                reply_markup=markup
            )
            await state.clear()
            return

        if user["farm"]["coconut"]["id"] != coco_data["id"]:
            update_data = {
                "coconut_balance": user["coconut_balance"] - total_price,
                "farm": {
                    "coconut": {"id": coco_data["id"]},
                    "coconuts_count": quantity
                }
            }
            if UserRequests.patch(message.from_user.id, update_data):
                await message.answer(
                    "✅ <b>Вы успешно приобрели кокосы!</b>\n\n"
                    "<b>Ваши предыдущие оставшиеся кокосы были сожжены!</b>",
                    parse_mode="HTML",
                    reply_markup=markup
                )
        else:
            update_data = {
                "coconut_balance": user["coconut_balance"] - total_price,
                "farm": {
                    "coconuts_count": quantity + user["farm"]["coconuts_count"]
                }
            }
            if UserRequests.patch(message.from_user.id, update_data):
                await message.answer(
                    "✅ <b>Вы успешно приобрели кокосы!</b>",
                    parse_mode="HTML",
                    reply_markup=markup
                )

        await state.clear()


class DonateStore:
    @staticmethod
    async def donate_store(callback_query: types.CallbackQuery, state: FSMContext | None = None):
        if state:
            await state.clear()

        buttons = [[InlineKeyboardButton(text="🕊️ Пожертвование", callback_data="donate_sum_input_handler")],
                   [InlineKeyboardButton(text="🥥 Экспериментальные кокосы",
                                         callback_data="experimental_coconuts_seems")],
                   [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_stores_menu")]]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text(f"🏬 <b>Добро пожаловать в donate магазин!</b>\n"
                                               f"\n"
                                               f"Здесь можно попытать себя в удаче или пожертововать разработчику "
                                               f"на пропитание!", parse_mode="HTML", reply_markup=markup
                                               )

    @staticmethod
    async def donate_sum_input_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await state.set_state(StoreStates.input_quantity)
        await state.update_data(callback_data=callback_query.data)
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="donate_store")]])
        await callback_query.message.edit_text("✍️ <b>Введите сумму Вашего пожертвования:</b>", parse_mode="HTML",
                                               reply_markup=markup)

    @staticmethod
    async def donate(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        amount = state_data['quantity']
        payment_data = PaymentRequests.create({
            "amount": amount,
            "telegram_id": message.from_user.id,
            "description": "Пожертвование проекту CocoTrade Project",
            "is_donate": True,
        })

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Проверить статус", callback_data=f"check_payment.{payment_data['id']}")]])

        await message.answer("🫂 <b>Спасибо за Ваше решение пожертвовать проекту копейку!</b>\n"
                             "\n"
                             f"<b>Ваша ссылка для оплаты - {payment_data['confirmation']['confirmation_url']}</b>",
                             parse_mode="HTML", reply_markup=markup)
        await state.clear()

    @staticmethod
    async def check_payment_status(callback_query: types.CallbackQuery):
        payment_id = callback_query.data.split(".")[1]
        payment = PaymentRequests.get(payment_id)
        payment_status = payment['status']

        if not payment_status:
            await callback_query.answer("❌ Ошибка при проверке статуса платежа", show_alert=True)
            return

        if payment_status == "succeeded":
            UserRequests.patch(callback_query.from_user.id, {"rub_balance": payment['amount']['value']})
            DonationRequests.create({"donator_id": callback_query.from_user.id, "amount": payment['amount']['value']})
            await callback_query.message.edit_text(
                "✅ <b>Спасибо за ваше пожертвование!</b>\n\n"
                "Ваша поддержка помогает развивать проект!",
                parse_mode="HTML"
            )
        elif payment_status == "pending":
            await callback_query.answer("⏳ Платеж все еще обрабатывается", show_alert=True)
        else:
            await callback_query.answer("❌ Платеж не был выполнен", show_alert=True)


@store_router.message(StoreStates.input_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError

        await state.update_data(quantity=quantity)
        match state_data['callback_data']:
            case "coconuts_seems":
                await CommonStore.buy_chosen_coconut(message, state)
            case "donate_sum_input_handler":
                await DonateStore.donate(message, state)
    except ValueError:
        markup = None
        match state_data['callback_data']:
            case "coconut_seems":
                coco = state_data['chosen_coco']
                markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"chosen_coco_view.{coco['id']}")]])
            case "donate_sum_input_handler":
                markup = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="donate_store")]])
        await message.answer("❗ <b>Введено неверное значение!</b>", parse_mode="HTML", reply_markup=markup)
        await state.set_state(StoreStates.selecting_item)


async def get_chosen_item(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    item_id = int(callback_query.data.split(".")[1])
    return [coco for coco in state_data["coconuts_data"] if coco["id"] == item_id][0]
