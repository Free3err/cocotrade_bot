from ....utils import DatabaseUtils
from ..models import User


class UserHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, user_id: int | None = None, telegram_id: int | None = None) -> User | None:
        if user_id:
            return session.query(User).filter(User.id == user_id).one_or_none()
        elif telegram_id:
            return session.query(User).filter(User.telegram_id == telegram_id).one_or_none()
        return None

    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, telegram_id: int) -> User:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
