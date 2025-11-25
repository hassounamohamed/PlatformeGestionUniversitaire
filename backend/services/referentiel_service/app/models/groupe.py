from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Groupe(Base):
    __tablename__ = "groupes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)
    niveau_id = Column(Integer, ForeignKey("niveaux.id"), nullable=True)
    departement_id = Column(Integer, ForeignKey("departements.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relations
    niveau = relationship("Niveau", back_populates="groupes")
    etudiants = relationship("Etudiant", back_populates="groupe")
