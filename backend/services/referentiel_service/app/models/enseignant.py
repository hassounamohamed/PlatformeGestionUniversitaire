from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class Enseignant(Base):
    __tablename__ = "enseignants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    departement_id = Column(Integer, ForeignKey("departements.id"), nullable=True)
