from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # metric name e.g. "attendance_rate"
    value = Column(Float, nullable=False)
    details = Column(String, nullable=True)  # JSON string with details (optional)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
