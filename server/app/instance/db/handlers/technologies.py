from typing import List

from ..models import Technology
from ....utils import DatabaseUtils


class TechnologyHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get_all(session) -> List[Technology] | None:
        return session.query(Technology).all()

    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, technology_id: int) -> Technology | None:
        return session.query(Technology).filter(Technology.id == technology_id).one_or_none()
    
    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, name: str, description: str, multiplier: int = 1) -> Technology:
        technology = Technology(name=name, description=description, multiplier=multiplier)
        session.add(technology)
        session.flush()
        session.refresh(technology)
        return technology
