from ..models import Role
from ....utils import DatabaseUtils

class RoleHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, role_id: int) -> Role:
        return session.query(Role).filter(Role.id == role_id).one_or_none()

