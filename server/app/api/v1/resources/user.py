from datetime import datetime

from flask import make_response, request
from flask_restx import Resource

from ....instance.db.handlers import UserHandler, FarmHandler
from ....utils import DatabaseUtils


class User(Resource):
    @staticmethod
    def get(telegram_id):
        user = UserHandler.get(telegram_id=telegram_id)
        if user:
            user_data = user.full_data()
            return make_response({"ok": True, "data": user_data}, 200)
        return make_response({"ok": False, "data": None, "message": "User doesn't exist"}, 404)

    @staticmethod
    def post(telegram_id):
        farm = FarmHandler.create()
        user = UserHandler.create(telegram_id=telegram_id, farm_id=farm.id)
        if user:
            user_data = DatabaseUtils.object_to_dict(user)
            return make_response({"ok": True, "data": user_data}, 200)
        else:
            return make_response({"ok": False, "message": "Failed to create user"}, 404)

    @staticmethod
    def delete(telegram_id):
        is_ok = UserHandler().remove(telegram_id=telegram_id)
        if is_ok:
            return make_response({"ok": True}, 200)
        return make_response({"ok": False, "message": "Failed to delete user"}, 502)

    @staticmethod
    def patch(telegram_id):
        response = request.json
        if "registered_at" in response:
            response["registered_at"] = datetime.fromisoformat(response["registered_at"])

        user = UserHandler().update(telegram_id=telegram_id, data=response)
        if user:
            user_data = user.full_data()
            return make_response({"ok": True, "data": user_data}, 200)
        return make_response({"ok": False, "message": "User doesn't exist"}, 404)


class UserList(Resource):
    @staticmethod
    def get():
        users = UserHandler.get_all()
        if users:
            users_datas = [user.full_data() for user in users]
            return make_response({"ok": True, "data": users_datas}, 200)
        return make_response({"ok": False, "message": "No enough user has found"}, 404)