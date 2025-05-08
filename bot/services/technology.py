import requests

from bot.config import EnvConfig


class TechnologyRequests:
    @staticmethod
    def get_all() -> dict | None:
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/technologies")

        if response.status_code == 200:
            return response.json()['data']
        return None
