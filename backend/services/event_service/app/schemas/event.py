from pydantic import BaseModel, ConfigDict
from datetime import datetime


class EventBase(BaseModel):
    titre: str
    type: str
    date: datetime
    description: str | None = None


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
