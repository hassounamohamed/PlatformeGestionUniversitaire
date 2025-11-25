from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Niveau(Base):
    __tablename__ = "niveaux"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)
    departement_id = Column(Integer, ForeignKey("departements.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relations
    groupes = relationship("Groupe", back_populates="niveau", cascade="all, delete-orphan")
