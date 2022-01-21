from sqlalchemy import Boolean, Column, Integer, String, JSON

from .database import Base


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    city_id = Column(String, nullable=False)
    state_id = Column(String)
    country_id = Column(String)
    conditions = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
