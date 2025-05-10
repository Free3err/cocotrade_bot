from typing import List

from ..models import Coconut
from ....utils import DatabaseUtils


class CoconutHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get_all(session) -> List[Coconut] | None:
        return session.query(Coconut).all()

    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, coconut_id: int) -> Coconut | None:
        return session.query(Coconut).filter(Coconut.id == coconut_id).one_or_none()

    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, name: str, description: str, amount_per_hour: int, is_experimental: bool = False) -> Coconut:
        coconut = Coconut(name=name, description=description, amount_per_hour=amount_per_hour,
                          is_experimental=is_experimental)
        session.add(coconut)
        session.commit()
        session.refresh(coconut)
        return coconut
