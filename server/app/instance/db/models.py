from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)
    coconut_balance = Column(Integer, default=0)
    rub_balance = Column(Integer, default=0)

    role = relationship("Role", back_populates="users")
    farm = relationship("Farm", back_populates="owner", uselist=False)
    location = relationship("UserLocation", back_populates="user", uselist=False)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class Farm(Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    level = Column(Integer, default=1)
    technology = Column(String, default='basic', nullable=False)
    coconut_type = Column(String, default='standard', nullable=False)

    owner = relationship("User", back_populates="farm")


class Coconut(Base):
    __tablename__ = 'coconuts'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    count_per_hour = Column(Integer, nullable=False)


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)


class UserLocation(Base):
    __tablename__ = 'user_locations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    arrived_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="location")
    location = relationship("Location")


class Market(Base):
    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    coconut_seed_type = Column(String, nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(Integer, nullable=False)

    seller = relationship("User")


class MarketTransaction(Base):
    __tablename__ = 'market_transactions'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    item = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    seller = relationship("User", foreign_keys=seller_id)
    buyer = relationship("User", foreign_keys=buyer_id)


class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
