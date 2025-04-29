from server.app.utils import DatabaseUtils
from ..models import Location


class LocationHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, location_id: int) -> dict | None:
        location = session.query(Location).filter(Location.id == location_id).one_or_none()
        return location
