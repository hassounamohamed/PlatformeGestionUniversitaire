from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    id_expediteur: int
    id_destinataire: int
    contenu: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)
