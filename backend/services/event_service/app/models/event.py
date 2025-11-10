from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=True)
