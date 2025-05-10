import json
import re

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
        dispatcher.callback_query.register(AdminManagingAccount.prompt_data_handler, F.data == "newsletter")

    @staticmethod
    async def admin(callback_query: CallbackQuery, state: FSMContext):
        await state.clear()

        buttons = [
            [InlineKeyboardButton(text="👤 Пользователь", callback_data="manage_user")],
            [InlineKeyboardButton(text="🎭 Роль", callback_data="manage_role"),
             InlineKeyboardButton(text="🏬 Магазин", callback_data="manage_stores_item")],
            [InlineKeyboardButton(text="📢 Рассылка", callback_data="newsletter")],
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
    async def newsletter(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        content = state_data["new_property"]

        users_ids = list([user["telegram_id"] for user in UserRequests.get_all() if user['is_subscribed_on_spam']])

        await message.answer("✅ <b>Рассылка начата!</b>", parse_mode="HTML")

        for user_id in users_ids:
            try:
                if isinstance(content, dict):
                    text = get_escaped_text(content["text"])
                    if content['type'] == 'photo':
                        await message.bot.send_photo(
                            chat_id=user_id,
                            photo=content['file_id'],
                            caption=text,
                            parse_mode="MarkdownV2"
                        )
                    elif content['type'] == 'video':
                        await message.bot.send_video(
                            chat_id=user_id,
                            video=content['file_id'],
                            caption=text,
                            parse_mode="MarkdownV2"
                        )
                    elif content['type'] == 'document':
                        await message.bot.send_document(
                            chat_id=user_id,
                            document=content['file_id'],
                            caption=text,
                            parse_mode="MarkdownV2"
                        )
                else:
                    await message.bot.send_message(
                        chat_id=user_id,
                        text=get_escaped_text(content),
                        parse_mode="MarkdownV2"
                    )

            except Exception as e:
                error_msg = f"Ошибка при отправке пользователю `{user_id}`:\n```\n{e}\n```"
                await message.answer(error_msg, parse_mode="MarkdownV2")

        await message.answer("✅ <b>Рассылка окончена!</b>", parse_mode="HTML")

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
            await callback_query.bot.send_message(user_id,
                                                  f"❗ <b>Ваш аккаунт в CocoTrade был удален <a href='tg://user?id={callback_query.from_user.id}'>администратором</a>!</b>",
                                                  parse_mode="HTML")
        else:
            await callback_query.message.edit_text("❌ <b>Не удалось удалить пользователя</b>", parse_mode="HTML",
                                                   reply_markup=markup)
        await state.clear()

    @staticmethod
    async def manage_coconut_balance(message: Message, state: FSMContext) -> None:
        state_data = await state.get_data()
        user_id = int(state_data['user_id'])
        new_coconut_balance = int(state_data['new_property'])

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
        new_ruble_balance = int(state_data['new_property'])

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
        new_user_json = json.loads(state_data['new_property'])

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
        elif callback_query.data == "newsletter":
            await callback_query.message.edit_text("✍️ <b>Введите текст рассылки (можно прикреплять медиа):</b>",
                                                   parse_mode="HTML", reply_markup=markup)


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
    state_data = await state.get_data()
    await state.update_data(new_property=message.text)

    match state_data.get("callback_data"):
        case "manage_coconut_balance":
            await AdminManagingAccount.manage_coconut_balance(message, state)
        case "manage_ruble_balance":
            await AdminManagingAccount.manage_ruble_balance(message, state)
        case "import_json_profile":
            await AdminManagingAccount.import_json_profile(message, state)
        case "newsletter":
            if not message.text:
                media_data = {
                    'type': None,
                    'file_id': None,
                    'text': message.caption if message.caption else ""
                }

                if message.photo:
                    media_data.update({
                        'type': 'photo',
                        'file_id': message.photo[-1].file_id
                    })
                elif message.video:
                    media_data.update({
                        'type': 'video',
                        'file_id': message.video.file_id
                    })
                elif message.document:
                    media_data.update({
                        'type': 'document',
                        'file_id': message.document.file_id
                    })
                await state.update_data(new_property=media_data)
            else:
                await state.update_data(new_property=message.text)
            await Admin.newsletter(message, state)
    await state.clear()


def get_escaped_text(text: str) -> str:
    escaped_text = text.translate(str.maketrans({
        '_': r'\_', '*': r'\*', '[': r'\[', ']': r'\]', '(': r'\(',
        ')': r'\)', '~': r'\~', '`': r'\`', '#': r'\#',
        '+': r'\+', '-': r'\-', '=': r'\=', '|': r'\|', '{': r'\{',
        '}': r'\}', '.': r'\.', '!': r'\!'
    }))
    processed_text = re.sub(r'<b>(.*?)</b>', r'*\1*', escaped_text)
    processed_text = re.sub(r'<i>(.*?)</i>', r'_\1_', processed_text)
    processed_text = re.sub(r'<code>(.*?)</code>', r'`\1`', processed_text)
    processed_text = re.sub(r'<pre>(.*?)</pre>', r'```\1```', processed_text)
    processed_text = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', processed_text)
    processed_text = re.sub(r'<blockquote>(.*?)</blockquote>',
                            lambda m: '>' + m.group(1).replace('\n', '\n>'),
                            processed_text, flags=re.DOTALL)
    return processed_text
