from datetime import datetime
from ..models import Conference
from ....utils import DatabaseUtils


class ConferenceHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, conference_id: int) -> Conference | None:
        return session.query(Conference).filter(Conference.id == conference_id).one_or_none()
    
    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, name: str, description: str, time_start: datetime) -> Conference:
        conference = Conference(name=name, description=description, time_start=time_start)
        session.add(conference)
        session.commit()
        session.refresh(conference)
        return conference 