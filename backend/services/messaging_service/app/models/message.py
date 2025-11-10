from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    id_expediteur = Column(Integer, nullable=False, index=True)
    id_destinataire = Column(Integer, nullable=False, index=True)
    contenu = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
