import requests

from bot.config import EnvConfig


class UserRequests:
    @staticmethod
    def get(telegram_id):
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/user/{telegram_id}")
        if response.status_code == 200:
            return response.json()["data"]
        return {}

    @staticmethod
    def register(telegram_id):
        response = requests.post(f"{EnvConfig.API_HOST}/api/v1/user/{telegram_id}")
        if response.status_code == 200:
            return response.json()["data"]
        return {}
