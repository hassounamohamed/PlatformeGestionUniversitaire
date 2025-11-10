from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class EmploiTemps(Base):
    __tablename__ = "emploi_temps"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    heure_debut = Column(Time, nullable=False)
    heure_fin = Column(Time, nullable=False)
    salle_id = Column(Integer, ForeignKey("salles.id"), nullable=False)
    matiere_id = Column(Integer, nullable=True)
    groupe_id = Column(Integer, nullable=True)
    enseignant_id = Column(Integer, nullable=True)

    salle = relationship("Salle", backref="emploi_entries")
