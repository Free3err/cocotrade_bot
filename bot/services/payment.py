import requests

from bot.config import EnvConfig


class PaymentRequests:
    @staticmethod
    def create(data: dict) -> dict:
        response = requests.post(f"{EnvConfig.API_HOST}/api/v1/payment", json=data)

        if response.status_code == 200:
            return response.json()['data']
        return {}

    @staticmethod
    def get(payment_id: str) -> dict:
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/payment/{payment_id}")
        
        if response.status_code == 200:
            return response.json()['data']
        return {}
