from flask import make_response
from flask_restx import Resource

from ....instance.db.handlers import UserHandler
from ....utils import DatabaseUtils


class User(Resource):
    @staticmethod
    def get(telegram_id):
        user = UserHandler().get(telegram_id=telegram_id)
        if user:
            user_data = DatabaseUtils.object_to_dict(user)
            return make_response({"ok": True, "data": user_data}, 200)
        return make_response({"ok": False, "data": None, "message": "User doesn't exist"}, 404)

    @staticmethod
    def post(telegram_id):
        user = UserHandler().create(telegram_id=telegram_id)
        if user:
            user_data = DatabaseUtils.object_to_dict(user)
            return make_response({"ok": True, "data": user_data}, 200)
        else:
            return make_response({"ok": False, "message": "Failed to create user"}, 404)

    @staticmethod
    def delete(telegram_id):
        pass

    @staticmethod
    def put(telegram_id):
        pass
