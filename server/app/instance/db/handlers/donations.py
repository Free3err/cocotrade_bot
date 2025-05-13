from typing import List

from server.app.utils import DatabaseUtils
from ..models import Donation


class DonationsHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get_all(session) -> List[Donation] | None:
        return session.query(Donation).all()

    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, donator_id: int, amount: int) -> Donation | None:
        donation = Donation(donator=donator_id, amount=amount)
        if donation:
            session.add(donation)
            session.commit()
            session.refresh(donation)
            return donation
        return None
