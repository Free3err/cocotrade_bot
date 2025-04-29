import requests

from bot.config import EnvConfig


class LocationRequests:
    @staticmethod
    def get(location_id):
        response = requests.get(f"{EnvConfig.API_HOST}/api/v1/location/{location_id}")
        if response.status_code == 200:
            return response.json()["data"]
        return {}