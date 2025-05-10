import requests

from bot.config import EnvConfig


class CoconutRequests:
    @staticmethod
    def get_all() -> dict:
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/coconuts")
        if response.status_code == 200:
            return response.json()["data"]
        return {}