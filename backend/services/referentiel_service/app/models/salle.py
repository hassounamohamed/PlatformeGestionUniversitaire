from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Salle(Base):
    __tablename__ = "salles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
