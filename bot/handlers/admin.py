from aiogram import Dispatcher, F, Router, types
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

admin_router = Router()


class AdminStates(StatesGroup):
    waiting_for_id = State()


class Admin:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.include_router(admin_router)

        dispatcher.callback_query.register(Admin.admin, F.data == "admin_panel")
        dispatcher.callback_query.register(Admin.prompt_id_handler, F.data == "manage_user")
        dispatcher.callback_query.register(Admin.prompt_id_handler, F.data == "manage_role")
        dispatcher.callback_query.register(Admin.prompt_id_handler, F.data == "manage_stores_item")

    @staticmethod
    async def admin(callback_query: CallbackQuery, state: FSMContext):
        await state.clear()

        buttons = [
            [InlineKeyboardButton(text="👤 Пользователь", callback_data="manage_user")],
            [InlineKeyboardButton(text="🎭 Роли", callback_data="manage_role"),
             InlineKeyboardButton(text="🏬 Магазин", callback_data="manage_stores_item")]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.edit_text(
            "🧑‍💻 <b>Добро пожаловать в админ-панель!</b>\n\n"
            "Вы можете управлять следующими параметрами:",
            parse_mode="HTML",
            reply_markup=markup
        )

    @staticmethod
    async def manage_user(message: types.Message, user_id):
        await message.answer(f"{user_id}")

    @staticmethod
    async def manage_role(message: types.Message, role_id):
        await message.answer(f"{role_id}")

    @staticmethod
    async def manage_stores_item(message: types.Message, store_item_id):
        await message.answer(f"{store_item_id}")

    @staticmethod
    async def prompt_id_handler(callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(AdminStates.waiting_for_id)
        await state.update_data(callback_data=callback_query.data)

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_panel")]
        ])

        await callback_query.message.edit_text(
            f"✍️ <b>Введите ID элемента</b>",
            parse_mode="HTML",
            reply_markup=markup
        )


@admin_router.message(AdminStates.waiting_for_id)
async def process_id_input(message: Message, state: FSMContext):
    user_input = message.text
    await state.update_data(entity_id=user_input)
    data = await state.get_data()
    entity_id = data.get("entity_id")
    await state.clear()

    match data.get("callback_data"):
        case "manage_user":
            await Admin.manage_user(message, entity_id)
        case "manage_role":
            await Admin.manage_role(message, entity_id)
        case "manage_stores_item":
            await Admin.manage_stores_item(message, entity_id)
