import requests

from bot.config import EnvConfig


class UserRequests:
    @staticmethod
    def get_all():
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/users")
        if response.status_code == 200:
            return response.json()['data']
        return {}

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

    @staticmethod
    def delete(telegram_id):
        response = requests.delete(f"{EnvConfig.API_HOST}/api/v1/user/{telegram_id}")
        if response.status_code == 200:
            return True
        return False

    @staticmethod
    def patch(telegram_id, data):
        response = requests.patch(f"{EnvConfig.API_HOST}/api/v1/user/{telegram_id}", json=data)
        if response.status_code == 200:
            return True
        return False
