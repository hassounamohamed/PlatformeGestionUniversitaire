from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Rattrapage(Base):
    __tablename__ = "rattrapages"

    id = Column(Integer, primary_key=True, index=True)
    absence_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    heure_debut = Column(Time, nullable=False)
    heure_fin = Column(Time, nullable=False)
    salle_id = Column(Integer, nullable=True)
