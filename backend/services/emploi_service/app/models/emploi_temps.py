from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
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
    # New text fields for display
    matiere_nom = Column(String, nullable=True)
    enseignant_nom = Column(String, nullable=True)
    groupe_nom = Column(String, nullable=True)  # e.g., TI14, DSI21

    salle = relationship("Salle", backref="emploi_entries")
