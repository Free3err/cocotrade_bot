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
    def create(session, telegram_id: int, farm_id: int) -> User:
        user = User(telegram_id=telegram_id, farm=farm_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    @DatabaseUtils.db_transaction
    def remove(session, user_id: int | None = None, telegram_id: int | None = None) -> True:
        user = session.query(User).filter(User.telegram_id == telegram_id).one_or_none()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

    @staticmethod
    @DatabaseUtils.db_transaction
    def update(session, telegram_id, data):
        from .farms import FarmHandler
        
        user = session.query(User).filter(User.telegram_id == telegram_id).one_or_none()
        if not user:
            return None
            
        for key, value in data.items():
            if key == 'farm' and isinstance(value, dict):
                FarmHandler.update(farm_id=user.farm, data=value)
            else:
                setattr(user, key, value)
                
        session.commit()
        session.refresh(user)
        return user
