from flask import make_response
from flask_restful import Resource


class User(Resource):
    @staticmethod
    def get(telegram_id):
        return make_response({}, 200)

    @staticmethod
    async def post(telegram_id):
        pass

    @staticmethod
    async def delete(telegram_id):
        pass

    @staticmethod
    async def put(telegram_id):
        pass
