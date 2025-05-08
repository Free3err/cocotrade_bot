import json

from aiogram import Dispatcher, F, Router, types
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.services import UserRequests

admin_router = Router()


class AdminStates(StatesGroup):
    waiting_for_id = State()
    user_managing = State()
    waiting_for_data = State()


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
            [InlineKeyboardButton(text="🎭 Роль", callback_data="manage_role"),
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
    async def manage_user(message: types.Message, state: FSMContext, user_id):
        user = UserRequests.get(user_id)
        if user:
            await state.set_state(AdminStates.user_managing)
            await state.update_data(user_id=user_id, user_data=user)
            buttons = [[InlineKeyboardButton(text="🗑️ Удалить пользователя", callback_data="admin_delete_account")],
                       [InlineKeyboardButton(text="🥥 Кокосовый баланс", callback_data="manage_coconut_balance"),
                        InlineKeyboardButton(text="💵 Рублевый баланс", callback_data="manage_ruble_balance")],
                       [InlineKeyboardButton(text="📥 Импортировать новый JSON-профиль",
                                             callback_data="import_json_profile")]]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.answer(f"📇 *Данные о пользователе с ID {user['id']}*\n"
                                 f"\n"
                                 f"```\n{json.dumps(user, indent=2, ensure_ascii=False)}\n```", parse_mode="MarkdownV2",
                                 reply_markup=markup)
        else:
            buttons = [[InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")]]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer("❌ <b>Пользователь с указанным ID не найден!</b>", parse_mode='HTML',
                                 reply_markup=markup)

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


class AdminManagingAccount:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(AdminManagingAccount.delete_account, F.data == 'admin_delete_account')
        dispatcher.callback_query.register(AdminManagingAccount.prompt_data_handler, F.data == 'manage_coconut_balance')
        dispatcher.callback_query.register(AdminManagingAccount.prompt_data_handler, F.data == 'manage_ruble_balance')
        dispatcher.callback_query.register(AdminManagingAccount.prompt_data_handler, F.data == 'import_json_profile')

    @staticmethod
    async def delete_account(callback_query: CallbackQuery, state: FSMContext) -> None:
        state_data = await state.get_data()
        user_id = int(state_data['user_id'])

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")], ])
        if UserRequests.delete(user_id):
            await callback_query.message.edit_text("✅ <b>Пользователь успешно удален!</b>", parse_mode="HTML",
                                                   reply_markup=markup)
        else:
            await callback_query.message.edit_text("❌ <b>Не удалось удалить пользователя</b>", parse_mode="HTML",
                                                   reply_markup=markup)
        await state.clear()

    @staticmethod
    async def manage_coconut_balance(message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        user_id = int(state_data['user_id'])
        new_coconut_balance = state_data['new_property']

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")], ])
        if UserRequests.patch(user_id, {'coconut_balance': new_coconut_balance}):
            await message.answer("✅ <b>Успешно изменен кокосовый баланс пользователя!</b>", parse_mode="HTML",
                                 reply_markup=markup)
        else:
            await message.answer("❌ <b>Не удалось изменить кокосовый баланс пользователя!</b>", parse_mode="HTML",
                                 reply_markup=markup)

    @staticmethod
    async def manage_ruble_balance(message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        user_id = int(state_data['user_id'])
        new_ruble_balance = state_data['new_property']

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")], ])
        if UserRequests.patch(user_id, {'rub_balance': new_ruble_balance}):
            await message.answer("✅ <b>Успешно изменен рублевый баланс пользователя!</b>", parse_mode="HTML",
                                 reply_markup=markup)
        else:
            await message.answer("❌ <b>Не удалось изменить рублевый баланс пользователя!</b>", parse_mode="HTML",
                                 reply_markup=markup)

    @staticmethod
    async def import_json_profile(message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        user_id = int(state_data['user_id'])
        new_user_json = state_data['new_property']

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")], ])
        if UserRequests.patch(user_id, new_user_json):
            await message.answer("✅ <b>Успешно импортирован новый профиль пользователя!</b>", parse_mode="HTML",
                                 reply_markup=markup)
        else:
            await message.answer("❌ <b>Не удалось импортировать JSON-профиль!</b>", parse_mode="HTML",
                                 reply_markup=markup)

    @staticmethod
    async def prompt_data_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(AdminStates.waiting_for_data)
        await state.update_data(callback_data=callback_query.data)

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_panel")]
        ])

        if callback_query.data in ["manage_coconut_balance", "manage_ruble_balance"]:
            await callback_query.message.edit_text("✍️ <b>Введите будущий баланс пользователя:</b>", parse_mode="HTML",
                                                   reply_markup=markup)
        elif callback_query.data == "import_json_profile":
            await callback_query.message.edit_text("✍️ <b>Введите JSON-профиль:</b>", parse_mode="HTML",
                                                   reply_markup=markup)


@admin_router.message(AdminStates.waiting_for_id)
async def process_id_input(message: Message, state: FSMContext):
    user_input = message.text
    await state.update_data(entity_id=user_input)
    data = await state.get_data()
    entity_id = data.get("entity_id")
    await state.clear()

    match data.get("callback_data"):
        case "manage_user":
            await Admin.manage_user(message, state, entity_id)
        case "manage_role":
            await Admin.manage_role(message, entity_id)
        case "manage_stores_item":
            await Admin.manage_stores_item(message, entity_id)


@admin_router.message(AdminStates.waiting_for_data)
async def process_data(message: Message, state: FSMContext):
    new_property = int(message.text)
    state_data = await state.get_data()
    await state.update_data(new_property=new_property)

    match state_data.get("callback_data"):
        case "manage_coconut_balance":
            await AdminManagingAccount.manage_coconut_balance(message, state)
        case "manage_ruble_balance":
            await AdminManagingAccount.manage_ruble_balance(message, state)
    await state.clear()
