from typing import List

from server.app.utils import DatabaseUtils
from ..models import Donation


class DonationsHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get_all(session) -> List[Donation] | None:
        return session.query(Donation).all()
