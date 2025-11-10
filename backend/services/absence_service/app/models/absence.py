from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Absence(Base):
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, nullable=False)
    emploi_id = Column(Integer, nullable=True)
    motif = Column(String, nullable=True)
    statut = Column(String, default="pending")  # pending | validated | rejected
