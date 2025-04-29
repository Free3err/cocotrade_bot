import logging
from datetime import datetime
from uuid import UUID

from ..instance.db import db


class DatabaseUtils:
    @staticmethod
    def db_transaction(func):
        def wrapper(*args, **kwargs):
            db_session = db.get_session()
            kwargs['session'] = db_session
            try:
                return func(*args, **kwargs)
            except Exception as e:
                db.rollback(session=db_session)
                logging.error(e)
                return None

        return wrapper

    @staticmethod
    def object_to_dict(object) -> dict:
        attrs = {}
        for attr, value in object.__dict__.items():
            if not attr.startswith('_'):
                if isinstance(value, UUID) or isinstance(value, datetime):
                    attrs[attr] = str(value)
                else:
                    attrs[attr] = value
        return attrs