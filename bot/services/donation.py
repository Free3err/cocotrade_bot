import requests

from bot.config import EnvConfig


class DonationRequests:
    @staticmethod
    def create(data) -> dict:
        response = requests.post(f"{EnvConfig.API_HOST}/api/v1/donation", json=data)
        if response.status_code == 200:
            return response.json()['data']
        return {}