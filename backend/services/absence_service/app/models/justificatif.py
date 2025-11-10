from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Justificatif(Base):
    __tablename__ = "justificatifs"

    id = Column(Integer, primary_key=True, index=True)
    absence_id = Column(Integer, nullable=False)
    file_path = Column(String, nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now())
    statut = Column(String, default="pending")  # pending | accepted | rejected
