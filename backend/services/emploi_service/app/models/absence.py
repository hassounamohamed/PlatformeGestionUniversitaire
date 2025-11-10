from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Absence(Base):
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    motif = Column(String, nullable=True)
