import asyncio

from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery

from ..services import UserRequests
from .main_menu import MainMenu


class ManagingAccount:
    @staticmethod
    def register_all(dispatcher: Dispatcher):
        dispatcher.callback_query.register(ManagingAccount.delete_account, F.data == 'delete_account')
        dispatcher.callback_query.register(ManagingAccount.subscribe_on_spam, F.data == 'subscribe_on_spam')
        dispatcher.callback_query.register(ManagingAccount.unsubscribe_on_spam, F.data == 'unsubscribe_on_spam')

    @staticmethod
    async def delete_account(callback_query: CallbackQuery) -> None:
        if UserRequests.delete(callback_query.from_user.id):
            await callback_query.message.edit_text("<b>Ваш аккаунт в CocoTrade успешно удален!</b>", parse_mode="HTML")
            await asyncio.sleep(5)
            await callback_query.message.edit_text(
                "<b>Учтите, что функционал бота не будет работоспособен до тех пор, пока вы вновь не нажмете /start!</b>",
                parse_mode="HTML", reply_markup=None)
        else:
            await callback_query.answer("Не удалось удалить аккаунт!")

    @staticmethod
    async def subscribe_on_spam(callback_query: CallbackQuery) -> None:
        if UserRequests.patch(callback_query.from_user.id, {'is_subscribed_on_spam': True}):
            await callback_query.answer("Вы успешно подписались на рассылки!")
            await MainMenu.settings(callback_query)
        else:
            await callback_query.answer("Не удалось подписаться на рассылки!")

    @staticmethod
    async def unsubscribe_on_spam(callback_query: CallbackQuery) -> None:
        if UserRequests.patch(callback_query.from_user.id, {'is_subscribed_on_spam': False}):
            await callback_query.answer("Вы успешно отписались от рассылок!")
            await MainMenu.settings(callback_query)
        else:
            await callback_query.answer("Не удалось отписаться от рассылок!")