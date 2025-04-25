from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import DatabaseConfig
from models import Base


class Database:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DatabaseConfig.DATABASE_URI}?check_same_thread=False", echo='info')
        self.SessionLocal = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine)
        self.init_schema()

    def init_schema(self) -> None:
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def commit(self, session) -> None:
        """Commit changes"""
        session.commit()

    def rollback(self, session) -> None:
        """Rollback changes"""
        session.rollback()