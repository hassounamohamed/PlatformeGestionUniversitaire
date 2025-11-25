from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    groupe_id = Column(Integer, ForeignKey("groupes.id"), nullable=True)
    specialite_id = Column(Integer, ForeignKey("matieres.id"), nullable=True)
    
    # Relations
    groupe = relationship("Groupe", back_populates="etudiants")

