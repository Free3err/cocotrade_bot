from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, String, REAL
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    role = Column(Integer, default=1)
    coconut_balance = Column(Integer, default=500)
    rub_balance = Column(Integer, default=0)
    farm = Column(Integer, ForeignKey('farms.id'), nullable=False)
    location = Column(Integer, default=1)
    is_subscribed_on_spam = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.now, nullable=False)

    farm_relation = relationship("Farm", uselist=False, cascade="all, delete-orphan", single_parent=True)

    def full_data(self):
        from .handlers import RoleHandler, LocationHandler, FarmHandler
        from ...utils import DatabaseUtils

        user_data = DatabaseUtils.object_to_dict(self)
        user_data['location'] = DatabaseUtils.object_to_dict(LocationHandler.get(location_id=self.location))
        user_data['role'] = DatabaseUtils.object_to_dict(RoleHandler.get(role_id=self.role))
        user_data['farm'] = FarmHandler.get(farm_id=self.farm).full_data()

        return user_data


class Farm(Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True)
    coconut = Column(Integer, ForeignKey('coconuts.id'), nullable=False, default=1)
    coconuts_count = Column(Integer, default=0)
    technology = Column(Integer, ForeignKey('technologies.id'), nullable=False, default=1)
    uncollected = Column(Integer, default=0, nullable=False)

    coconut_relation = relationship("Coconut", uselist=False)
    technology_relation = relationship("Technology", uselist=False)

    def full_data(self):
        from ...utils import DatabaseUtils

        farm_data = DatabaseUtils.object_to_dict(self)
        farm_data['coconut'] = DatabaseUtils.object_to_dict(self.coconut_relation)
        farm_data['technology'] = DatabaseUtils.object_to_dict(self.technology_relation)

        return farm_data


class Technology(Base):
    __tablename__ = 'technologies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    multiplier = Column(REAL, default=1)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Coconut(Base):
    __tablename__ = 'coconuts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount_per_hour = Column(Integer, nullable=False)
    is_experimental = Column(Boolean, default=False)


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Conference(Base):
    __tablename__ = 'conferences'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time_start = Column(DateTime, nullable=False)
