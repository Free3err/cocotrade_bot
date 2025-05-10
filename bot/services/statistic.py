import requests

from bot.config import EnvConfig


class StatisticRequests:
    @staticmethod
    def get() -> dict:
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/statistic")
        if response.status_code == 200:
            return response.json()['data']
        return {}
