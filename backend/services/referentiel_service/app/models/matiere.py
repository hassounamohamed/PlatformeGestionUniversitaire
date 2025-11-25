from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Matiere(Base):
    __tablename__ = "matieres"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=True)
    niveau_id = Column(Integer, ForeignKey("niveaux.id"), nullable=True)
    enseignant_id = Column(Integer, ForeignKey("enseignants.id"), nullable=True)
    departement_id = Column(Integer, ForeignKey("departements.id"), nullable=True)
